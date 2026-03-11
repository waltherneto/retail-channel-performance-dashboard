from etl.extract import extract_sales_csv
from etl.transform import save_processed_data, transform_sales_data

RAW_INPUT_FILE = "data/raw/retail_sales_raw.csv"
PROCESSED_OUTPUT_FILE = "data/processed/retail_sales_clean.csv"

def main() -> None:
  """
  Run the extract-and-transform stage of the retail sales pipeline.
  """
  print("Starting retail sales pipeline...")
  print(f"Reading raw dataset from: {RAW_INPUT_FILE}")

  df_raw = extract_sales_csv(RAW_INPUT_FILE)
  print(f"Raw rows extracted: {len(df_raw)}")

  df_clean, summary = transform_sales_data(df_raw)
  save_processed_data(df_clean, PROCESSED_OUTPUT_FILE)

  print(f"Processed dataset saved to: {PROCESSED_OUTPUT_FILE}")
  print("Transformation summary:")

  for key, value in summary.items():
    print(f" - {key}: {value}")

  print("Extract and transform stage completed successfully.")

if __name__ == "__main__":
  main()