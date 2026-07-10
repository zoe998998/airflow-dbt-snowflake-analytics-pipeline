from datetime import timedelta
import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator


AIRFLOW_HOME = "/opt/airflow"
DBT_PROJECT_DIR = "/opt/airflow/dbt_retail_pipeline"
DBT_PROFILES_DIR = "/home/airflow/.dbt"

local_tz = pendulum.timezone("Asia/Shanghai")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="retail_analytics_pipeline",
    default_args=default_args,
    start_date=pendulum.datetime(2026, 6, 28, tz=local_tz),
    schedule="0 2 * * *", # every day at 02:00 in local timezone
    catchup=False,
    max_active_runs=1,
    tags=["snowflake", "dbt", "retail"],
) as dag:

    generate_sample_data = BashOperator(
        task_id="generate_sample_data",
        bash_command=f"cd {AIRFLOW_HOME} && python scripts/etl/generate_sample_data.py",
    )

    load_to_snowflake = BashOperator(
        task_id="load_to_snowflake",
        bash_command=f"cd {AIRFLOW_HOME} && python scripts/etl/load_to_snowflake.py",
    )

    dbt_deps = BashOperator(
        task_id="dbt_deps",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt deps --profiles-dir {DBT_PROFILES_DIR}",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt run --profiles-dir {DBT_PROFILES_DIR}",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt test --profiles-dir {DBT_PROFILES_DIR}",
    )

    generate_sample_data >> load_to_snowflake >> dbt_deps >> dbt_run >> dbt_test