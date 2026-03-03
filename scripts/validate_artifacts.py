from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    ROOT / "data/interim/data_merged_clean.parquet",
    ROOT / "data/interim/sales_region_day_base.parquet",
    ROOT / "data/interim/sales_global_day_base.parquet",
    ROOT / "data/processed/train_region.parquet",
    ROOT / "data/processed/train_global.parquet",
    ROOT / "model_store/latest/ml_global/pipeline.joblib",
    ROOT / "model_store/latest/ml_region/pipeline.joblib",
    ROOT / "model_store/latest/ts_region",
]

missing = [str(p) for p in REQUIRED if not p.exists()]
if missing:
    raise FileNotFoundError("Artifacts manquants:\n- " + "\n- ".join(missing))

print("✅ Artifacts OK")