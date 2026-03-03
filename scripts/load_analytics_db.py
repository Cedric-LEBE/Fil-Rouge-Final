from __future__ import annotations

import os
import time
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[1]
PARQUET_PATH = ROOT / "data" / "interim" / "data_merged_clean.parquet"

DB_URL = os.getenv(
    "ANALYTICS_DATABASE_URL",
    # IMPORTANT: dans docker-compose, c’est analytics-db, pas localhost
    "postgresql+psycopg2://analytics:analytics@analytics-db:5432/analytics",
)

TABLE_NAME = os.getenv("ANALYTICS_TABLE", "sales")
MAX_RETRIES = int(os.getenv("DB_CONNECT_RETRIES", "30"))
SLEEP_SEC = float(os.getenv("DB_CONNECT_SLEEP", "2"))


def wait_for_db(engine) -> None:
    last_err = None
    for _ in range(MAX_RETRIES):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except Exception as e:
            last_err = e
            time.sleep(SLEEP_SEC)
    raise RuntimeError(f"DB not ready after retries. Last error: {last_err}")


def main() -> None:
    if not PARQUET_PATH.exists():
        raise FileNotFoundError(f"Missing parquet: {PARQUET_PATH}")

    df = pd.read_parquet(PARQUET_PATH)

    # Normalize column names: snake_case expected by SQL generator
    rename = {}
    for c in df.columns:
        cc = c.strip().lower().replace(" ", "_").replace("-", "_")
        rename[c] = cc
    df = df.rename(columns=rename)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    engine = create_engine(DB_URL, pool_pre_ping=True)
    wait_for_db(engine)

    # pgvector extension (si image pgvector)
    with engine.begin() as conn:
        try:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        except Exception:
            pass

    # load table
    df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False, chunksize=50_000, method="multi")

    # indexes
    with engine.begin() as conn:
        stmts = []
        if "date" in df.columns:
            stmts.append(f"CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_date ON {TABLE_NAME}(date)")
        if "region" in df.columns:
            stmts.append(f"CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_region ON {TABLE_NAME}(region)")
        if "macro_category" in df.columns:
            stmts.append(f"CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_macro_category ON {TABLE_NAME}(macro_category)")

        for stmt in stmts:
            try:
                conn.execute(text(stmt))
            except Exception:
                pass

    print(f"✅ Loaded analytics DB table: {TABLE_NAME} (rows={len(df):,})")


if __name__ == "__main__":
    main()