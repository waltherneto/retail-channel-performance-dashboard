import pandas as pd

def transform_sales_data(df: pd.DataFrame) -> pd.DataFrame:
  """
  Placeholder transformation function for retail sales data.

  Args:
    df: Raw sales DataFrame.

  Returns:
    Transformed DataFrame.
  """
  if df.empty:
    raise ValueError("Input DataFrame is empty.")

  return df.copy()