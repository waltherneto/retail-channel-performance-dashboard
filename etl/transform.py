from __future__ import annotations

from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = [
  "transaction_date",
  "region",
  "distributor",
  "store",
  "sales_channel",
  "product",
  "category",
  "units_sold",
  "revenue",
]

TEXT_COLUMNS = [
  "region",
  "distributor",
  "store",
  "sales_channel",
  "product",
  "category",
]

def validate_required_columns(df: pd.DataFrame) -> None:
  """
  Ensure all expected columns exist in the dataset.

  Args:
    df: Input DataFrame.

  Raises:
    ValueError: If one or more required columns are missing.
  """
  missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

  if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")


def standardize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
  """
  Trim and normalize spacing in text columns.

  Args:
    df: Input DataFrame.

  Returns:
    DataFrame with normalized text columns.
  """
  df = df.copy()

  for col in TEXT_COLUMNS:
    df[col] = (
      df[col]
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

  return df

def cast_column_types(df: pd.DataFrame) -> pd.DataFrame:
  """
  Cast dataset columns to appropriate data types.

  Args:
    df: Input DataFrame.

  Returns:
    DataFrame with converted types.
  """
  df = df.copy()

  df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
  df["units_sold"] = pd.to_numeric(df["units_sold"], errors="coerce")
  df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")

  return df

def remove_invalid_rows(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
  """
  Remove rows that violate basic business and data quality rules.

  Rules:
  - Required fields cannot be null
  - transaction_date must be valid
  - units_sold must be > 0
  - revenue must be > 0

  Args:
    df: Input DataFrame.

  Returns:
    Tuple containing:
    - Cleaned DataFrame
    - Dictionary with counts of removed rows by rule
  """
  df = df.copy()
  initial_row_count = len(df)

  null_required_mask = df[REQUIRED_COLUMNS].isnull().any(axis=1)
  invalid_date_mask = df["transaction_date"].isnull()
  invalid_units_mask = df["units_sold"].isnull() | (df["units_sold"] <= 0)
  invalid_revenue_mask = df["revenue"].isnull() | (df["revenue"] <= 0)

  invalid_mask = (
    null_required_mask
    | invalid_date_mask
    | invalid_units_mask
    | invalid_revenue_mask
  )

  removed_counts = {
    "rows_with_null_required_fields": int(null_required_mask.sum()),
    "rows_with_invalid_dates": int(invalid_date_mask.sum()),
    "rows_with_invalid_units": int(invalid_units_mask.sum()),
    "rows_with_invalid_revenue": int(invalid_revenue_mask.sum()),
  }

  df = df.loc[~invalid_mask].copy()

  removed_counts["rows_removed_total_before_dedup"] = initial_row_count - len(df)

  return df, removed_counts

def remove_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
  """
  Remove exact duplicate rows.

  Args:
    df: Input DataFrame.

  Returns:
    Tuple containing:
    - DataFrame without duplicates
    - Number of duplicates removed
  """
  df = df.copy()
  initial_row_count = len(df)

  df = df.drop_duplicates()

  duplicates_removed = initial_row_count - len(df)

  return df, duplicates_removed

def finalize_output(df: pd.DataFrame) -> pd.DataFrame:
  """
  Final formatting before writing the processed dataset.

  Args:
    df: Cleaned DataFrame.

  Returns:
    Final processed DataFrame.
  """
  df = df.copy()

  df["transaction_date"] = df["transaction_date"].dt.strftime("%Y-%m-%d")
  df["units_sold"] = df["units_sold"].astype(int)
  df["revenue"] = df["revenue"].round(2)

  df = df.sort_values(
      by=["transaction_date", "region", "distributor", "store", "product"]
  ).reset_index(drop=True)

  return df

def save_processed_data(df: pd.DataFrame, output_path: str) -> None:
  """
  Save processed data to CSV.

  Args:
    df: Processed DataFrame.
    output_path: Destination path.
  """
  path = Path(output_path)
  path.parent.mkdir(parents=True, exist_ok=True)
  df.to_csv(path, index=False)

def transform_sales_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
  """
  Transform and validate raw retail sales data.

  Args:
    df: Raw sales DataFrame.

  Returns:
    Tuple containing:
    - Processed DataFrame
    - Transformation summary statistics
  """
  if df.empty:
    raise ValueError("Input DataFrame is empty.")

  validate_required_columns(df)

  initial_rows = len(df)

  df = standardize_text_columns(df)
  df = cast_column_types(df)

  df, removal_stats = remove_invalid_rows(df)
  df, duplicates_removed = remove_duplicates(df)
  df = finalize_output(df)

  summary = {
    "initial_rows": initial_rows,
    "final_rows": len(df),
    "rows_removed_total": initial_rows - len(df),
    "duplicates_removed": duplicates_removed,
    **removal_stats,
  }

  return df, summary