FROM apache/airflow:2.11.0-python3.12

USER airflow

RUN pip install --no-cache-dir \
    dbt-core==1.9.0 \
    dbt-snowflake==1.9.0 \
    snowflake-connector-python \
    pandas