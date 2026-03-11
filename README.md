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

## Status

In progress.