# Retail Channel Performance Dashboard

A portfolio Data Engineering project that simulates how raw retail sales data can be transformed into an analytical model for Power BI reporting.

## Tech Stack

- Python
- Pandas
- PostgreSQL
- SQL
- Power BI

## Project Goal

Build a small end-to-end data pipeline that transforms raw retail transaction data into a star schema analytical model for retail performance reporting.

## Business Scenario

A consumer goods company sells products through distributors and retail stores. Management needs visibility into sell-in and sell-out performance across regions, distributors, product categories, and channels.

## Planned Pipeline

CSV dataset  
→ Python ETL  
→ Data cleaning and validation  
→ PostgreSQL warehouse  
→ Star schema analytical model  
→ Power BI dashboard

## Repository Structure

```text
retail-channel-performance-dashboard/
├── data/
├── etl/
├── sql/
├── dashboard/
├── screenshots/
├── docs/
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

## Dataset

The project uses a synthetic retail sales dataset generated with Python to simulate a realistic consumer goods distribution scenario.

### Raw dataset fields

- transaction_date
- region
- distributor
- store
- sales_channel
- product
- category
- units_sold
- revenue

### Dataset characteristics

- Covers multiple regions
- Includes several distributors and stores
- Simulates product and category mix
- Includes different sales channels
- Applies volume variability by channel
- Adds small price fluctuations to simulate real commercial behavior

## Environment Setup

Create and activate a virtual environment, then install the project dependencies:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## ETL Pipeline

The ETL pipeline is organized into modular Python components:

- `extract.py` reads the raw CSV dataset
- `transform.py` standardizes, validates, and cleans the data
- `run_pipeline.py` orchestrates the extract-and-transform stage
- the processed dataset is written to `data/processed/retail_sales_clean.csv`

### Data quality rules applied

- required columns validation
- text standardization
- date parsing and validation
- numeric type enforcement
- positive value checks for `units_sold`
- positive value checks for `revenue`
- duplicate removal

## Warehouse Load

After data cleaning, the processed dataset is loaded into PostgreSQL in two stages:

1. `stg_retail_sales` receives the cleaned transactional data
2. SQL scripts populate the analytical star schema:
   - `dim_date`
   - `dim_region`
   - `dim_product`
   - `dim_distributor`
   - `dim_store`
   - `dim_channel`
   - `fact_sales`

The loading logic is orchestrated by `etl/load.py`, which:
- reads database credentials from environment variables
- truncates tables for repeatable local execution
- loads staging data from CSV
- executes SQL scripts for dimensions and fact loading
- returns row-count summaries after execution

## Data Quality and Validation

The project includes SQL-based quality checks to validate the consistency of the warehouse after loading.

### Validation coverage
- row-count reconciliation between staging and fact tables
- revenue reconciliation
- units sold reconciliation
- null foreign key checks
- duplicate grain checks
- invalid value checks
- quick outlier inspection

### Analytical validation queries
Additional SQL queries were used to validate:
- monthly revenue trends
- regional revenue distribution
- category performance
- top products
- distributor performance
- sales channel performance

## Notes

For simplicity in this portfolio project, all tables were created in the default PostgreSQL public schema. In a production environment, staging and analytics objects would typically be separated into dedicated schemas. 

## Status

In progress.