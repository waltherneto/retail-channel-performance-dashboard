-- Load fact table from staging and dimensions

INSERT INTO fact_sales (
  date_key,
  region_key,
  product_key,
  distributor_key,
  store_key,
  channel_key,
  units_sold,
  revenue
)
SELECT
    TO_CHAR(s.transaction_date, 'YYYYMMDD')::INTEGER AS date_key,
    r.region_key,
    p.product_key,
    d.distributor_key,
    st.store_key,
    c.channel_key,
    s.units_sold,
    s.revenue
FROM stg_retail_sales s
INNER JOIN dim_region r
    ON s.region = r.region_name
INNER JOIN dim_product p
    ON s.product = p.product_name
   AND s.category = p.category
INNER JOIN dim_distributor d
    ON s.distributor = d.distributor_name
INNER JOIN dim_store st
    ON s.store = st.store_name
INNER JOIN dim_channel c
    ON s.sales_channel = c.channel_name;