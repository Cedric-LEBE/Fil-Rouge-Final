from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from fil_rouge.config import (
    PROCESSED_DIR,
    MODEL_STORE,
    DATE_COL,
    TARGET_COL,
    GROUP_COL,
    TEST_SIZE,
    RANDOM_STATE,
)
from fil_rouge.io import read_parquet
from fil_rouge.train import benchmark_train_and_save


def main() -> None:
    train_path = PROCESSED_DIR / "train.parquet"
    if not train_path.exists():
        raise FileNotFoundError(f"Missing: {train_path}")

    df = read_parquet(train_path)

    leaderboard, run_dir, best_name = benchmark_train_and_save(
        df,
        model_store=MODEL_STORE,
        date_col=DATE_COL,
        target_col=TARGET_COL,
        group_col=GROUP_COL,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    print("\n✅ Leaderboard (top 5):")
    print(leaderboard.head(5).to_string(index=False))
    print(f"\n🏆 Best model: {best_name}")
    print(f"📦 Run saved: {run_dir}")
    print(f"⭐ Latest updated: {MODEL_STORE / 'latest'}")


if __name__ == "__main__":
    main()