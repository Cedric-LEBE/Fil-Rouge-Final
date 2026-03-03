from __future__ import annotations

import os
import sys
from pathlib import Path

import mlflow

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from fil_rouge.pipelines.ts.train_ts_region import run_train_ts_region

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "retail_forecast")

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)


if __name__ == "__main__":
    with mlflow.start_run(run_name="train_ts_region"):
        run_train_ts_region()