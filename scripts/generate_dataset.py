from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import random

import pandas as pd

@dataclass(frozen=True)
class Product:
  name: str
  category: str
  unit_price: float

def build_reference_data() -> tuple[list[str], dict[str, list[str]], dict[str, list[str]], list[Product], list[str]]:
  """
  Create static business reference data used to simulate retail transactions.

  Returns:
    regions: List of regions.
    distributors_by_region: Mapping of region -> distributors.
    stores_by_region: Mapping of region -> stores.
    products: List of product definitions.
    sales_channels: List of sales channels.
  """
  regions = [
    "North",
    "Northeast",
    "Central-West",
    "Southeast",
    "South",
  ]

  distributors_by_region = {
    "North": ["Amazon Distribution", "Norte Supply"],
    "Northeast": ["Nordeste Partners", "Coastal Distribution"],
    "Central-West": ["Cerrado Logistics", "MidBrasil Supply"],
    "Southeast": ["SP Trade Hub", "Atlântico Distribuição", "Rio Valley Distribution"],
    "South": ["SulMax Distribuidora", "Pampa Supply"],
  }

  stores_by_region = {
    "North": ["Manaus Retail Center", "Belém Market Point", "Porto Velho Outlet"],
    "Northeast": ["Recife Store Hub", "Salvador Retail Point", "Fortaleza Market Center"],
    "Central-West": ["Goiânia Sales Point", "Brasília Retail Hub", "Cuiabá Store Center"],
    "Southeast": ["São Paulo Prime Store", "Campinas Retail Hub", "Rio Market Center", "Belo Horizonte Outlet"],
    "South": ["Curitiba Retail Point", "Porto Alegre Store Hub", "Florianópolis Market Center"],
  }

  products = [
    Product("Classic Soda 350ml", "Beverages", 4.50),
    Product("Orange Juice 1L", "Beverages", 7.90),
    Product("Mineral Water 500ml", "Beverages", 2.80),
    Product("Potato Chips 120g", "Snacks", 6.50),
    Product("Peanut Mix 200g", "Snacks", 8.20),
    Product("Chocolate Bar 90g", "Confectionery", 5.40),
    Product("Cookies Pack 140g", "Confectionery", 6.80),
    Product("Tomato Sauce 340g", "Grocery", 4.20),
    Product("Pasta 500g", "Grocery", 5.90),
    Product("Laundry Detergent 1L", "Household", 12.50),
    Product("Dish Soap 500ml", "Household", 4.90),
    Product("Paper Towels 2-roll", "Household", 8.70),
  ]

  sales_channels = [
    "Cash & Carry",
    "Supermarket",
    "Convenience",
    "Pharmacy",
    "E-commerce",
  ]

  return regions, distributors_by_region, stores_by_region, products, sales_channels


def random_transaction_date(start_date: datetime, end_date: datetime) -> datetime:
  """
  Generate a random transaction datetime between two dates.

  Args:
    start_date: Inclusive lower bound.
    end_date: Inclusive upper bound.

  Returns:
    Random datetime between start_date and end_date.
  """
  delta_days = (end_date - start_date).days
  random_days = random.randint(0, delta_days)
  return start_date + timedelta(days=random_days)


def generate_sales_dataset(row_count: int = 10_000, seed: int = 42) -> pd.DataFrame:
  """
  Generate a synthetic retail sales dataset.

  Args:
    row_count: Number of rows to generate.
    seed: Seed for reproducibility.

  Returns:
    Pandas DataFrame with simulated retail sales transactions.
  """
  random.seed(seed)
  (
      regions,
      distributors_by_region,
      stores_by_region,
      products,
      sales_channels,
  ) = build_reference_data()

  start_date = datetime(2024, 1, 1)
  end_date = datetime(2024, 12, 31)

  records: list[dict] = []

  for _ in range(row_count):
    region = random.choice(regions)
    distributor = random.choice(distributors_by_region[region])
    store = random.choice(stores_by_region[region])
    sales_channel = random.choice(sales_channels)
    product = random.choice(products)

    transaction_date = random_transaction_date(start_date, end_date)

    # Small business logic to create more plausible sales volumes by channel
    channel_units_range = {
      "Cash & Carry": (15, 120),
      "Supermarket": (10, 80),
      "Convenience": (3, 25),
      "Pharmacy": (2, 20),
      "E-commerce": (1, 18),
    }

    min_units, max_units = channel_units_range[sales_channel]
    units_sold = random.randint(min_units, max_units)

    # Revenue generated with slight price variation to simulate discounts / negotiations
    unit_price_variation = random.uniform(0.92, 1.08)
    unit_price = round(product.unit_price * unit_price_variation, 2)
    revenue = round(units_sold * unit_price, 2)

    records.append(
      {
        "transaction_date": transaction_date.strftime("%Y-%m-%d"),
        "region": region,
        "distributor": distributor,
        "store": store,
        "sales_channel": sales_channel,
        "product": product.name,
        "category": product.category,
        "units_sold": units_sold,
        "revenue": revenue,
      }
    )

  df = pd.DataFrame(records)

  return df


def save_dataset(df: pd.DataFrame, output_path: str) -> None:
  """
  Save the generated dataset to CSV.

  Args:
    df: Dataset to save.
    output_path: Destination file path.
  """
  path = Path(output_path)
  path.parent.mkdir(parents=True, exist_ok=True)
  df.to_csv(path, index=False)


def main() -> None:
  """
  Generate and save the retail sales raw dataset.
  """
  output_file = "data/raw/retail_sales_raw.csv"

  df = generate_sales_dataset(row_count=10_000, seed=42)
  save_dataset(df, output_file)

  print("Dataset generated successfully.")
  print(f"Output file: {output_file}")
  print(f"Rows generated: {len(df)}")
  print("\nSample:")
  print(df.head(10).to_string(index=False))


if __name__ == "__main__":
  main()