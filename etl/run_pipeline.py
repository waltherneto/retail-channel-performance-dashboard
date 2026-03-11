from etl.extract import extract_sales_csv
from etl.transform import transform_sales_data


def main() -> None:
  input_file = "data/raw/retail_sales_raw.csv"

  df_raw = extract_sales_csv(input_file)
  df_transformed = transform_sales_data(df_raw)

  print("Pipeline executed successfully.")
  print(f"Raw rows: {len(df_raw)}")
  print(f"Transformed rows: {len(df_transformed)}")


if __name__ == "__main__":
  main()