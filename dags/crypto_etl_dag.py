from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

default_args = {
    "owner": "kiran",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="crypto_etl_pipeline_split",
    default_args=default_args,
    description="Crypto ETL pipeline split into extract, transform, and load tasks",
    schedule="@daily",
    start_date=datetime(2026, 4, 1),
    catchup=False,
    tags=["crypto", "etl", "postgres"],
) as dag:

    extract_task = BashOperator(
        task_id="extract_task",
        bash_command="cd /opt/airflow/project/scripts && python extract.py",
    )

    transform_task = BashOperator(
        task_id="transform_task",
        bash_command="cd /opt/airflow/project/scripts && python transform.py",
    )

    load_task = BashOperator(
        task_id="load_task",
        bash_command="cd /opt/airflow/project/scripts && python load.py",
    )

    extract_task >> transform_task >> load_task