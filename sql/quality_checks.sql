-- Retail Channel Performance Dashboard
-- Data quality, reconciliation, and analytical validation checks

-- ============================================
-- 1. ROW COUNT RECONCILIATION
-- ============================================

SELECT 'staging_row_count' AS check_name, COUNT(*) AS row_count
FROM stg_retail_sales

UNION ALL

SELECT 'fact_row_count' AS check_name, COUNT(*) AS row_count
FROM fact_sales;


-- ============================================
-- 2. REVENUE RECONCILIATION
-- ============================================

SELECT
  'staging_revenue' AS metric_source,
  ROUND(SUM(revenue), 2) AS total_revenue
FROM stg_retail_sales

UNION ALL

SELECT
  'fact_revenue' AS metric_source,
  ROUND(SUM(revenue), 2) AS total_revenue
FROM fact_sales;


-- ============================================
-- 3. UNITS SOLD RECONCILIATION
-- ============================================

SELECT
  'staging_units' AS metric_source,
  SUM(units_sold) AS total_units_sold
FROM stg_retail_sales

UNION ALL

SELECT
  'fact_units' AS metric_source,
  SUM(units_sold) AS total_units_sold
FROM fact_sales;


-- ============================================
-- 4. NULL CHECKS IN FACT TABLE FOREIGN KEYS
-- ============================================

SELECT
  SUM(CASE WHEN date_key IS NULL THEN 1 ELSE 0 END) AS null_date_keys,
  SUM(CASE WHEN region_key IS NULL THEN 1 ELSE 0 END) AS null_region_keys,
  SUM(CASE WHEN product_key IS NULL THEN 1 ELSE 0 END) AS null_product_keys,
  SUM(CASE WHEN distributor_key IS NULL THEN 1 ELSE 0 END) AS null_distributor_keys,
  SUM(CASE WHEN store_key IS NULL THEN 1 ELSE 0 END) AS null_store_keys,
  SUM(CASE WHEN channel_key IS NULL THEN 1 ELSE 0 END) AS null_channel_keys
FROM fact_sales;


-- ============================================
-- 5. DUPLICATE BUSINESS GRAIN CHECK IN STAGING
-- ============================================

SELECT
  transaction_date,
  region,
  distributor,
  store,
  sales_channel,
  product,
  category,
  units_sold,
  revenue,
  COUNT(*) AS duplicate_count
FROM stg_retail_sales
GROUP BY
  transaction_date,
  region,
  distributor,
  store,
  sales_channel,
  product,
  category,
  units_sold,
  revenue
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;


-- ============================================
-- 6. NEGATIVE OR ZERO VALUE CHECKS
-- ============================================

SELECT
  SUM(CASE WHEN units_sold <= 0 THEN 1 ELSE 0 END) AS invalid_units_rows,
  SUM(CASE WHEN revenue <= 0 THEN 1 ELSE 0 END) AS invalid_revenue_rows
FROM fact_sales;


-- ============================================
-- 7. QUICK OUTLIER CHECKS
-- ============================================

SELECT
  MIN(units_sold) AS min_units_sold,
  MAX(units_sold) AS max_units_sold,
  ROUND(AVG(units_sold), 2) AS avg_units_sold,
  MIN(revenue) AS min_revenue,
  MAX(revenue) AS max_revenue,
  ROUND(AVG(revenue), 2) AS avg_revenue
FROM fact_sales;


-- ============================================
-- 8. MONTHLY REVENUE TREND
-- ============================================

SELECT
  d.year,
  d.month,
  d.month_name,
  ROUND(SUM(f.revenue), 2) AS monthly_revenue,
  SUM(f.units_sold) AS monthly_units_sold
FROM fact_sales f
JOIN dim_date d
  ON f.date_key = d.date_key
GROUP BY
  d.year,
  d.month,
  d.month_name
ORDER BY
  d.year,
  d.month;


-- ============================================
-- 9. REVENUE BY REGION
-- ============================================

SELECT
  r.region_name,
  ROUND(SUM(f.revenue), 2) AS total_revenue,
  SUM(f.units_sold) AS total_units_sold
FROM fact_sales f
JOIN dim_region r
  ON f.region_key = r.region_key
GROUP BY r.region_name
ORDER BY total_revenue DESC;


-- ============================================
-- 10. REVENUE BY CATEGORY
-- ============================================

SELECT
  p.category,
  ROUND(SUM(f.revenue), 2) AS total_revenue,
  SUM(f.units_sold) AS total_units_sold
FROM fact_sales f
JOIN dim_product p
  ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY total_revenue DESC;


-- ============================================
-- 11. TOP 10 PRODUCTS BY REVENUE
-- ============================================

SELECT
  p.product_name,
  p.category,
  ROUND(SUM(f.revenue), 2) AS total_revenue,
  SUM(f.units_sold) AS total_units_sold
FROM fact_sales f
JOIN dim_product p
  ON f.product_key = p.product_key
GROUP BY
  p.product_name,
  p.category
ORDER BY total_revenue DESC
LIMIT 10;


-- ============================================
-- 12. DISTRIBUTOR PERFORMANCE
-- ============================================

SELECT
  d.distributor_name,
  ROUND(SUM(f.revenue), 2) AS total_revenue,
  SUM(f.units_sold) AS total_units_sold,
  ROUND(AVG(f.revenue), 2) AS avg_row_revenue
FROM fact_sales f
JOIN dim_distributor d
  ON f.distributor_key = d.distributor_key
GROUP BY d.distributor_name
ORDER BY total_revenue DESC;


-- ============================================
-- 13. CHANNEL PERFORMANCE
-- ============================================

SELECT
  c.channel_name,
  ROUND(SUM(f.revenue), 2) AS total_revenue,
  SUM(f.units_sold) AS total_units_sold,
  ROUND(AVG(f.revenue), 2) AS avg_row_revenue
FROM fact_sales f
JOIN dim_channel c
  ON f.channel_key = c.channel_key
GROUP BY c.channel_name
ORDER BY total_revenue DESC;