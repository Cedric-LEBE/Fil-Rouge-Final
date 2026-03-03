from __future__ import annotations

from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {"owner": "airflow"}

with DAG(
    dag_id="retail_pipeline",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["retail", "ml"],
) as dag:

    make_dataset = BashOperator(
        task_id="make_dataset",
        bash_command="python /opt/project/scripts/make_dataset.py",
    )

    train_ml_global = BashOperator(
        task_id="train_ml_global",
        bash_command="python /opt/project/scripts/train_ml_global.py",
    )

    train_ml_region = BashOperator(
        task_id="train_ml_region",
        bash_command="python /opt/project/scripts/train_ml_region.py",
    )

    train_ts_region = BashOperator(
        task_id="train_ts_region",
        bash_command="python /opt/project/scripts/train_ts_region.py",
    )

    sanity_check = BashOperator(
        task_id="sanity_check",
        bash_command="python /opt/project/scripts/sanity_check.py",
    )

    validate_artifacts = BashOperator(
        task_id="validate_artifacts",
        bash_command="python /opt/project/scripts/validate_artifacts.py",
    )

    export_streamlit_bundle = BashOperator(
        task_id="export_streamlit_bundle",
        bash_command="python /opt/project/scripts/export_streamlit_bundle.py",
    )

    (
        make_dataset
        >> train_ml_global
        >> train_ml_region
        >> train_ts_region
        >> sanity_check
        >> validate_artifacts
        >> export_streamlit_bundle
    )