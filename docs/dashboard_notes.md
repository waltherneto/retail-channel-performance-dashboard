# Dashboard Notes

## Data Quality Summary

The warehouse quality checks confirmed that the pipeline loaded the analytical model consistently.

### Validation highlights
- staging and fact row counts reconciled successfully
- total revenue matched between staging and fact tables
- total units sold matched between staging and fact tables
- no null foreign keys were found in the fact table
- no invalid zero or negative values were found
- no duplicate rows were detected at the business grain level

## Analytical Highlights

### Revenue by region
Use the regional revenue results to support the Regional Performance dashboard page.

### Revenue by category
Use category aggregation to validate the Product Performance page.

### Top products
Use the top-10 revenue query to identify the best-performing products.

### Distributor performance
Use distributor ranking to support comparison visuals and KPI commentary.

### Channel performance
Use channel revenue and volume metrics to support dashboard slicing and segmentation.