-- Retail Channel Performance Dashboard
-- Schema creation script for staging and analytics layers

-- Optional cleanup for repeatable local development
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_channel;
DROP TABLE IF EXISTS dim_store;
DROP TABLE IF EXISTS dim_distributor;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_region;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS stg_retail_sales;

-- ============================================
-- 1. STAGING TABLE
-- ============================================

CREATE TABLE stg_retail_sales (
  transaction_id      BIGSERIAL PRIMARY KEY,
  transaction_date    DATE NOT NULL,
  region              VARCHAR(100) NOT NULL,
  distributor         VARCHAR(150) NOT NULL,
  store               VARCHAR(150) NOT NULL,
  sales_channel       VARCHAR(100) NOT NULL,
  product             VARCHAR(150) NOT NULL,
  category            VARCHAR(100) NOT NULL,
  units_sold          INTEGER NOT NULL CHECK (units_sold > 0),
  revenue             NUMERIC(12, 2) NOT NULL CHECK (revenue > 0)
);

-- ============================================
-- 2. DIMENSION TABLES
-- ============================================

CREATE TABLE dim_date (
  date_key            INTEGER PRIMARY KEY,
  full_date           DATE NOT NULL UNIQUE,
  year                INTEGER NOT NULL,
  quarter             INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
  month               INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
  month_name          VARCHAR(20) NOT NULL,
  day_of_month        INTEGER NOT NULL CHECK (day_of_month BETWEEN 1 AND 31),
  day_of_week         INTEGER NOT NULL CHECK (day_of_week BETWEEN 1 AND 7),
  day_name            VARCHAR(20) NOT NULL
);

CREATE TABLE dim_region (
  region_key          BIGSERIAL PRIMARY KEY,
  region_name         VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE dim_product (
  product_key         BIGSERIAL PRIMARY KEY,
  product_name        VARCHAR(150) NOT NULL,
  category            VARCHAR(100) NOT NULL,
  CONSTRAINT uq_dim_product UNIQUE (product_name, category)
);

CREATE TABLE dim_distributor (
  distributor_key     BIGSERIAL PRIMARY KEY,
  distributor_name    VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE dim_store (
  store_key           BIGSERIAL PRIMARY KEY,
  store_name          VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE dim_channel (
  channel_key         BIGSERIAL PRIMARY KEY,
  channel_name        VARCHAR(100) NOT NULL UNIQUE
);

-- ============================================
-- 3. FACT TABLE
-- ============================================

CREATE TABLE fact_sales (
  sales_key           BIGSERIAL PRIMARY KEY,
  date_key            INTEGER NOT NULL,
  region_key          BIGINT NOT NULL,
  product_key         BIGINT NOT NULL,
  distributor_key     BIGINT NOT NULL,
  store_key           BIGINT NOT NULL,
  channel_key         BIGINT NOT NULL,
  units_sold          INTEGER NOT NULL CHECK (units_sold > 0),
  revenue             NUMERIC(12, 2) NOT NULL CHECK (revenue > 0),

  CONSTRAINT fk_fact_sales_date
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),

  CONSTRAINT fk_fact_sales_region
    FOREIGN KEY (region_key) REFERENCES dim_region(region_key),

  CONSTRAINT fk_fact_sales_product
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),

  CONSTRAINT fk_fact_sales_distributor
    FOREIGN KEY (distributor_key) REFERENCES dim_distributor(distributor_key),

  CONSTRAINT fk_fact_sales_store
    FOREIGN KEY (store_key) REFERENCES dim_store(store_key),

  CONSTRAINT fk_fact_sales_channel
    FOREIGN KEY (channel_key) REFERENCES dim_channel(channel_key)
);

-- ============================================
-- 4. INDEXES
-- ============================================

CREATE INDEX idx_stg_transaction_date ON stg_retail_sales(transaction_date);
CREATE INDEX idx_stg_region ON stg_retail_sales(region);
CREATE INDEX idx_stg_product ON stg_retail_sales(product);
CREATE INDEX idx_stg_distributor ON stg_retail_sales(distributor);

CREATE INDEX idx_fact_sales_date_key ON fact_sales(date_key);
CREATE INDEX idx_fact_sales_region_key ON fact_sales(region_key);
CREATE INDEX idx_fact_sales_product_key ON fact_sales(product_key);
CREATE INDEX idx_fact_sales_distributor_key ON fact_sales(distributor_key);
CREATE INDEX idx_fact_sales_store_key ON fact_sales(store_key);
CREATE INDEX idx_fact_sales_channel_key ON fact_sales(channel_key);