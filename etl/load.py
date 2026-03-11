from __future__ import annotations

from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def get_database_connection_string() -> str:
  """
  Build a SQLAlchemy PostgreSQL connection string from environment variables.

  Returns:
    PostgreSQL connection string.

  Raises:
    ValueError: If one or more required environment variables are missing.
  """
  load_dotenv()

  required_vars = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
  missing_vars = [var for var in required_vars if not os.getenv(var)]

  if missing_vars:
    raise ValueError(
      f"Missing required database environment variables: {missing_vars}"
    )

  db_host = os.getenv("DB_HOST")
  db_port = os.getenv("DB_PORT")
  db_name = os.getenv("DB_NAME")
  db_user = os.getenv("DB_USER")
  db_password = os.getenv("DB_PASSWORD")

  return (
    f"postgresql+psycopg2://{db_user}:{db_password}"
    f"@{db_host}:{db_port}/{db_name}"
  )

def get_engine() -> Engine:
  """
  Create and return a SQLAlchemy engine for PostgreSQL.

  Returns:
      SQLAlchemy Engine instance.
  """
  connection_string = get_database_connection_string()
  return create_engine(connection_string)

def read_sql_file(file_path: str) -> str:
  """
  Read a SQL file from disk.

  Args:
      file_path: Path to the SQL file.

  Returns:
      SQL script content as string.
  """
  path = Path(file_path)

  if not path.exists():
      raise FileNotFoundError(f"SQL file not found: {file_path}")

  return path.read_text(encoding="utf-8")

def truncate_tables(engine: Engine) -> None:
  """
  Truncate staging and analytics tables in dependency-safe order.

  Args:
    engine: SQLAlchemy engine.
  """
  truncate_sql = """
  TRUNCATE TABLE
    fact_sales,
    dim_channel,
    dim_store,
    dim_distributor,
    dim_product,
    dim_region,
    dim_date,
    stg_retail_sales
  RESTART IDENTITY;
  """

  with engine.begin() as connection:
    connection.execute(text(truncate_sql))

def load_staging_data(engine: Engine, file_path: str) -> int:
  """
  Load processed CSV data into the staging table.

  Args:
    engine: SQLAlchemy engine.
    file_path: Path to processed CSV file.

  Returns:
    Number of rows loaded into staging.
  """
  path = Path(file_path)

  if not path.exists():
    raise FileNotFoundError(f"Processed data file not found: {file_path}")

  df = pd.read_csv(path)

  if df.empty:
    raise ValueError("Processed dataset is empty.")

  df["transaction_date"] = pd.to_datetime(df["transaction_date"])

  df.to_sql(
    name="stg_retail_sales",
    con=engine,
    if_exists="append",
    index=False,
    method="multi",
    chunksize=1000,
  )

  return len(df)

def execute_sql_script(engine: Engine, file_path: str) -> None:
  """
  Execute a SQL script file against the database.

  Args:
    engine: SQLAlchemy engine.
    file_path: Path to SQL script.
  """
  sql_script = read_sql_file(file_path)

  with engine.begin() as connection:
    connection.execute(text(sql_script))

def fetch_scalar(engine: Engine, query: str) -> int:
  """
  Execute a scalar query and return an integer result.

  Args:
    engine: SQLAlchemy engine.
    query: SQL query expected to return a single scalar value.

  Returns:
    Integer scalar result.
  """
  with engine.begin() as connection:
    result = connection.execute(text(query)).scalar()

  return int(result) if result is not None else 0

def get_load_summary(engine: Engine) -> dict[str, int]:
  """
  Collect basic row-count metrics after loading the warehouse.

  Args:
    engine: SQLAlchemy engine.

  Returns:
    Dictionary with row counts for staging, dimensions, and fact table.
  """
  return {
    "staging_rows": fetch_scalar(engine, "SELECT COUNT(*) FROM stg_retail_sales;"),
    "dim_date_rows": fetch_scalar(engine, "SELECT COUNT(*) FROM dim_date;"),
    "dim_region_rows": fetch_scalar(engine, "SELECT COUNT(*) FROM dim_region;"),
    "dim_product_rows": fetch_scalar(engine, "SELECT COUNT(*) FROM dim_product;"),
    "dim_distributor_rows": fetch_scalar(
        engine, "SELECT COUNT(*) FROM dim_distributor;"
    ),
    "dim_store_rows": fetch_scalar(engine, "SELECT COUNT(*) FROM dim_store;"),
    "dim_channel_rows": fetch_scalar(engine, "SELECT COUNT(*) FROM dim_channel;"),
    "fact_sales_rows": fetch_scalar(engine, "SELECT COUNT(*) FROM fact_sales;"),
  }

def load_warehouse(processed_file_path: str) -> dict[str, int]:
  """
  Run the full warehouse loading process:
  - truncate existing data
  - load staging
  - populate dimensions
  - populate fact table
  - return summary counts

  Args:
    processed_file_path: Path to the processed CSV file.

  Returns:
    Dictionary with load summary metrics.
  """
  engine = get_engine()

  truncate_tables(engine)
  load_staging_data(engine, processed_file_path)
  execute_sql_script(engine, "sql/load_dimensions.sql")
  execute_sql_script(engine, "sql/load_fact.sql")

  return get_load_summary(engine)