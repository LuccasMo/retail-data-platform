# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE VIEW retail.gold.vw_sales_analytics AS 
# MAGIC
# MAGIC SELECT
# MAGIC     f.sale_id,
# MAGIC     f.sale_timestamp,
# MAGIC
# MAGIC     d.date,
# MAGIC     d.year,
# MAGIC     d.month,
# MAGIC     d.day,
# MAGIC
# MAGIC     c.customer_id,
# MAGIC     c.name AS customer_name,
# MAGIC     c.city,
# MAGIC     c.state,
# MAGIC
# MAGIC     p.product_id,
# MAGIC     p.product_name,
# MAGIC     p.category,
# MAGIC     p.brand,
# MAGIC
# MAGIC     s.store_id,
# MAGIC     s.store_name,
# MAGIC     s.region,
# MAGIC
# MAGIC     f.quantity,
# MAGIC     f.unit_price,
# MAGIC     f.discount,
# MAGIC     f.gross_amount,
# MAGIC     f.net_amount,
# MAGIC     f.total_cost,
# MAGIC     f.profit,
# MAGIC     f.payment_method
# MAGIC
# MAGIC FROM retail.gold.fact_sales f
# MAGIC
# MAGIC LEFT JOIN retail.gold.dim_customers c
# MAGIC     ON f.customer_id = c.customer_id
# MAGIC
# MAGIC LEFT JOIN retail.gold.dim_products p
# MAGIC     ON f.product_id = p.product_id
# MAGIC
# MAGIC LEFT JOIN retail.gold.dim_stores s
# MAGIC     ON f.store_id = s.store_id
# MAGIC
# MAGIC LEFT JOIN retail.gold.dim_date d
# MAGIC     ON f.date_id = d.date_id;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM retail.gold.vw_sales_analytics
# MAGIC LIMIT 20;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     COUNT(DISTINCT sale_id) AS total_sales,
# MAGIC     ROUND(SUM(net_amount), 2) AS total_revenue,
# MAGIC     ROUND(SUM(profit), 2) AS total_profit,
# MAGIC
# MAGIC     ROUND(
# MAGIC         try_divide(
# MAGIC             SUM(profit) * 100,
# MAGIC             SUM(net_amount)
# MAGIC         ),
# MAGIC         2
# MAGIC     ) AS avg_profit_margin,
# MAGIC
# MAGIC     ROUND(AVG(net_amount), 2) AS avarage_ticket,
# MAGIC     SUM(quantity) AS units_sold
# MAGIC
# MAGIC FROM retail.gold.vw_sales_analytics;
# MAGIC     

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     date,
# MAGIC     ROUND(SUM(net_amount), 2) AS revenue,
# MAGIC     ROUND(SUM(profit), 2) AS profit
# MAGIC FROM retail.gold.vw_sales_analytics
# MAGIC GROUP BY date
# MAGIC ORDER BY date;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     region,
# MAGIC     ROUND(SUM(net_amount), 2) AS revenue,
# MAGIC     ROUND(SUM(profit), 2) AS profit,
# MAGIC     COUNT(DISTINCT sale_id) AS sales
# MAGIC FROM retail.gold.vw_sales_analytics
# MAGIC GROUP BY region
# MAGIC ORDER BY revenue DESC;
# MAGIC

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC SELECT
# MAGIC     category,
# MAGIC     SUM(quantity) AS units_sold,
# MAGIC     ROUND(SUM(net_amount), 2) AS revenue,
# MAGIC     ROUND(SUM(profit), 2) AS profit,
# MAGIC     ROUND(
# MAGIC         try_divide(
# MAGIC             SUM(profit) * 100,
# MAGIC             SUM(net_amount)
# MAGIC         ),
# MAGIC         2
# MAGIC     ) AS margin_pct
# MAGIC FROM retail.gold.vw_sales_analytics
# MAGIC GROUP BY category
# MAGIC ORDER BY revenue DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT 
# MAGIC     product_name,
# MAGIC     category,
# MAGIC     SUM(quantity) AS units_sold,
# MAGIC     ROUND(SUM(net_amount), 2) AS revenue,
# MAGIC     ROUND(SUM(profit), 2) AS profit
# MAGIC FROM retail.gold.vw_sales_analytics
# MAGIC GROUP BY
# MAGIC     product_name,
# MAGIC     category
# MAGIC ORDER BY revenue DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     store_name,
# MAGIC     region,
# MAGIC     COUNT(DISTINCT sale_id) AS sales,
# MAGIC     SUM(quantity) AS units_sold,
# MAGIC     ROUND(SUM(net_amount), 2) AS revenue,
# MAGIC     ROUND(SUM(profit), 2) AS profit
# MAGIC FROM retail.gold.vw_sales_analytics
# MAGIC GROUP BY
# MAGIC     store_name,
# MAGIC     region
# MAGIC ORDER BY revenue DESC
# MAGIC LIMIT 10;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     payment_method,
# MAGIC     COUNT(DISTINCT sale_id) AS sales,
# MAGIC     ROUND(SUM(net_amount), 2) AS revenue,
# MAGIC     ROUND(
# MAGIC         try_divide(
# MAGIC             COUNT(DISTINCT sale_id) * 100.0,
# MAGIC             SUM(COUNT(DISTINCT sale_id)) OVER ()
# MAGIC         ),
# MAGIC         2
# MAGIC     ) AS sales_share_pct
# MAGIC FROM retail.gold.vw_sales_analytics
# MAGIC GROUP BY payment_method
# MAGIC ORDER BY revenue DESC;