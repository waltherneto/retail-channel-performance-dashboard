from pathlib import Path
import pandas as pd

def extract_sales_csv(file_path: str) -> pd.DataFrame:
  """
  Read raw retail sales data from a CSV file.

  Args:
    file_path: Path to the input CSV file.

  Returns:
    A pandas DataFrame containing raw sales data.
  """
  path = Path(file_path)

  if not path.exists():
    raise FileNotFoundError(f"Input file not found: {file_path}")

  df = pd.read_csv(path)

  if df.empty:
    raise ValueError("Input CSV is empty.")

  return df