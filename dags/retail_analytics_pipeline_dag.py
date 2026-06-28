from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


AIRFLOW_HOME = "/opt/airflow"
DBT_PROJECT_DIR = "/opt/airflow/dbt_retail_pipeline"


with DAG(
    dag_id="retail_analytics_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["snowflake", "dbt", "retail"],
) as dag:

    generate_sample_data = BashOperator(
        task_id="generate_sample_data",
        bash_command=f"cd {AIRFLOW_HOME} && python scripts/generate_sample_data.py",
    )

    load_to_snowflake = BashOperator(
        task_id="load_to_snowflake",
        bash_command=f"cd {AIRFLOW_HOME} && python scripts/load_to_snowflake.py",
    )

    dbt_deps = BashOperator(
    task_id="dbt_deps",
    bash_command=f"cd {DBT_PROJECT_DIR} && dbt deps --profiles-dir /opt/airflow/.dbt",
    )

    dbt_run = BashOperator(
    task_id="dbt_run",
    bash_command=f"cd {DBT_PROJECT_DIR} && dbt run --profiles-dir /opt/airflow/.dbt",
    )

    dbt_test = BashOperator(
    task_id="dbt_test",
    bash_command=f"cd {DBT_PROJECT_DIR} && dbt test --profiles-dir /opt/airflow/.dbt",
    )

    generate_sample_data >> load_to_snowflake >> dbt_deps >> dbt_run >> dbt_test