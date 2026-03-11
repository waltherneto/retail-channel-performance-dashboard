-- Load analytical dimensions from staging layer

-- ============================================
-- 1. DATE DIMENSION
-- ============================================

INSERT INTO dim_date (
  date_key,
  full_date,
  year,
  quarter,
  month,
  month_name,
  day_of_month,
  day_of_week,
  day_name
)
SELECT DISTINCT
  TO_CHAR(transaction_date, 'YYYYMMDD')::INTEGER AS date_key,
  transaction_date AS full_date,
  EXTRACT(YEAR FROM transaction_date)::INTEGER AS year,
  EXTRACT(QUARTER FROM transaction_date)::INTEGER AS quarter,
  EXTRACT(MONTH FROM transaction_date)::INTEGER AS month,
  TO_CHAR(transaction_date, 'Month')::VARCHAR(20) AS month_name,
  EXTRACT(DAY FROM transaction_date)::INTEGER AS day_of_month,
  EXTRACT(ISODOW FROM transaction_date)::INTEGER AS day_of_week,
  TO_CHAR(transaction_date, 'Day')::VARCHAR(20) AS day_name
FROM stg_retail_sales;

-- Normalize padded names produced by TO_CHAR
UPDATE dim_date
SET
  month_name = TRIM(month_name),
  day_name = TRIM(day_name);

-- ============================================
-- 2. REGION DIMENSION
-- ============================================

INSERT INTO dim_region (region_name)
SELECT DISTINCT region
FROM stg_retail_sales
ORDER BY region;

-- ============================================
-- 3. PRODUCT DIMENSION
-- ============================================

INSERT INTO dim_product (product_name, category)
SELECT DISTINCT product, category
FROM stg_retail_sales
ORDER BY product, category;

-- ============================================
-- 4. DISTRIBUTOR DIMENSION
-- ============================================

INSERT INTO dim_distributor (distributor_name)
SELECT DISTINCT distributor
FROM stg_retail_sales
ORDER BY distributor;

-- ============================================
-- 5. STORE DIMENSION
-- ============================================

INSERT INTO dim_store (store_name)
SELECT DISTINCT store
FROM stg_retail_sales
ORDER BY store;

-- ============================================
-- 6. CHANNEL DIMENSION
-- ============================================

INSERT INTO dim_channel (channel_name)
SELECT DISTINCT sales_channel
FROM stg_retail_sales
ORDER BY sales_channel;