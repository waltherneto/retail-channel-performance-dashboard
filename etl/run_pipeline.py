from etl.extract import extract_sales_csv
from etl.load import load_warehouse
from etl.transform import save_processed_data, transform_sales_data

RAW_INPUT_FILE = "data/raw/retail_sales_raw.csv"
PROCESSED_OUTPUT_FILE = "data/processed/retail_sales_clean.csv"

def main() -> None:
  """
  Run the full retail sales pipeline:
  extract -> transform -> load to PostgreSQL warehouse.
  """
  print("Starting retail sales pipeline...")
  print(f"Reading raw dataset from: {RAW_INPUT_FILE}")

  df_raw = extract_sales_csv(RAW_INPUT_FILE)
  print(f"Raw rows extracted: {len(df_raw)}")

  df_clean, transform_summary = transform_sales_data(df_raw)
  save_processed_data(df_clean, PROCESSED_OUTPUT_FILE)

  print(f"Processed dataset saved to: {PROCESSED_OUTPUT_FILE}")
  print("Transformation summary:")
  for key, value in transform_summary.items():
    print(f" - {key}: {value}")

  print("Loading processed data into PostgreSQL warehouse...")
  load_summary = load_warehouse(PROCESSED_OUTPUT_FILE)

  print("Load summary:")
  for key, value in load_summary.items():
    print(f" - {key}: {value}")

  print("Pipeline completed successfully.")

if __name__ == "__main__":
  main()