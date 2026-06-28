import os
from pathlib import Path

import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
from snowflake.connector.pandas_tools import write_pandas


load_dotenv()

RAW_DATA_DIR = Path("data/raw")

TARGET_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
TARGET_SCHEMA = "RAW"
TARGET_TABLE = "OPERATIONS_RAW"


def get_snowflake_connection():
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=TARGET_DATABASE,
        schema=TARGET_SCHEMA,
    )


def read_raw_csv_files() -> pd.DataFrame:
    csv_files = sorted(RAW_DATA_DIR.glob("*_operations.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {RAW_DATA_DIR}")

    dataframes = []

    for file_path in csv_files:
        df = pd.read_csv(file_path)
        df["source_file"] = file_path.name
        dataframes.append(df)
        print(f"Read {file_path} | rows: {len(df)}")

    combined_df = pd.concat(dataframes, ignore_index=True)

    print(f"Combined rows: {len(combined_df)}")
    print(f"Combined columns before cleaning: {len(combined_df.columns)}")

    return combined_df


def prepare_dataframe_for_snowflake(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.upper() for col in df.columns]

    df["REPORT_DATE"] = pd.to_datetime(df["REPORT_DATE"]).dt.date

    if "SOURCE_FILE" in df.columns:
        df = df.drop(columns=["SOURCE_FILE"])

    print(f"Columns after cleaning: {len(df.columns)}")

    return df


def load_dataframe_to_snowflake(conn, df: pd.DataFrame):
    cursor = conn.cursor()
    full_table_name = f"{TARGET_DATABASE}.{TARGET_SCHEMA}.{TARGET_TABLE}"

    try:
        cursor.execute(f"TRUNCATE TABLE {full_table_name}")

        success, _, nrows, _ = write_pandas(
            conn=conn,
            df=df,
            table_name=TARGET_TABLE,
            database=TARGET_DATABASE,
            schema=TARGET_SCHEMA,
            quote_identifiers=False,
        )

        if not success:
            raise RuntimeError("write_pandas failed to load data into Snowflake.")

        cursor.execute(f"SELECT COUNT(*) FROM {full_table_name}")
        row_count = cursor.fetchone()[0]

        print(f"Loaded rows into Snowflake: {nrows}")
        print(f"Snowflake table row count: {row_count}")

    finally:
        cursor.close()


def main():
    conn = get_snowflake_connection()

    try:
        print("Successfully connected to Snowflake.")

        df = read_raw_csv_files()
        df = prepare_dataframe_for_snowflake(df)
        load_dataframe_to_snowflake(conn, df)

        print("CSV to Snowflake RAW load completed successfully.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()