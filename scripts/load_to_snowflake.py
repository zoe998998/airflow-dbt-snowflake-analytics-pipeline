import os
import pandas as pd
from dotenv import load_dotenv
import snowflake.connector

# Load .env
load_dotenv()

# Connect to Snowflake
conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    role=os.getenv("SNOWFLAKE_ROLE"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)

print("Successfully connected to Snowflake!")

# Test query
cursor = conn.cursor()
cursor.execute("SELECT CURRENT_VERSION()")

result = cursor.fetchone()

print("Snowflake Version:", result[0])

# Read CSV test
df = pd.read_csv("data/raw/east_operations.csv")

print(df.head())
print(f"Rows loaded: {len(df)}")

cursor.close()
conn.close()