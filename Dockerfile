FROM apache/airflow:2.11.0-python3.12

# Install operating-system dependency required by dbt deps
USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Return to the standard non-root Airflow user
USER airflow

RUN pip install --no-cache-dir \
    dbt-core==1.9.0 \
    dbt-snowflake==1.9.0 \
    snowflake-connector-python \
    pandas \
    numpy \
    python-dotenv