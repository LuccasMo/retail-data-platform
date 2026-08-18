# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC SELECT 'bronze_customers' AS tabela, COUNT(*) AS registros
# MAGIC FROM retail.bronze.customers_auto
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'bronze_products', COUNT(*)
# MAGIC FROM retail.bronze.products_auto
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'bronze_stores', COUNT(*)
# MAGIC FROM retail.bronze.stores_auto
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'bronze_sales', COUNT(*)
# MAGIC FROM retail.bronze.sales_auto
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'silver_customers', COUNT(*)
# MAGIC FROM retail.silver.customers
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'silver_products', COUNT(*)
# MAGIC FROM retail.silver.products
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'silver_stores', COUNT(*)
# MAGIC FROM retail.silver.stores
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'silver_sales', COUNT(*)
# MAGIC FROM retail.silver.sales
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'gold_fact_sales', COUNT(*)
# MAGIC FROM retail.gold.fact_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     COUNT(*) AS duplicated_sale_ids
# MAGIC FROM (
# MAGIC     SELECT
# MAGIC         sale_id
# MAGIC     FROM retail.gold.fact_sales
# MAGIC     GROUP BY sale_id
# MAGIC     HAVING COUNT(*) > 1
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_bronze,
# MAGIC     (
# MAGIC         SELECT COUNT(*)
# MAGIC         FROM retail.silver.sales
# MAGIC     ) AS total_valid,
# MAGIC     (
# MAGIC         SELECT COUNT(*)
# MAGIC         FROM retail.silver.sales_quarantine
# MAGIC     ) AS total_invalid;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC WITH totals AS (
# MAGIC     SELECT
# MAGIC         (SELECT COUNT(*) FROM retail.silver.sales) AS validos,
# MAGIC         (SELECT COUNT(*) FROM retail.silver.sales_quarantine) AS invalidos
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     validos,
# MAGIC     invalidos,
# MAGIC     validos + invalidos AS total_processado,
# MAGIC     ROUND(
# MAGIC         try_divide(invalidos * 100.0, validos + invalidos),
# MAGIC         2
# MAGIC     ) AS rejection_rate_pct
# MAGIC FROM totals;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT 'bronze_customers' AS tabela, COUNT(*) AS registros
# MAGIC FROM retail.bronze.customers_auto
# MAGIC
# MAGIC UNION ALL
# MAGIC SELECT 'bronze_products', COUNT(*) FROM retail.bronze.products_auto
# MAGIC
# MAGIC UNION ALL
# MAGIC SELECT 'bronze_stores', COUNT(*) FROM retail.bronze.stores_auto
# MAGIC
# MAGIC UNION ALL
# MAGIC SELECT 'bronze_sales', COUNT(*) FROM retail.bronze.sales_auto
# MAGIC
# MAGIC UNION ALL
# MAGIC SELECT 'silver_customers', COUNT(*) FROM retail.silver.customers
# MAGIC
# MAGIC UNION ALL
# MAGIC SELECT 'silver_products', COUNT(*) FROM retail.silver.products
# MAGIC
# MAGIC UNION ALL
# MAGIC SELECT 'silver_stores', COUNT(*) FROM retail.silver.stores
# MAGIC
# MAGIC UNION ALL
# MAGIC SELECT 'silver_sales', COUNT(*) FROM retail.silver.sales
# MAGIC
# MAGIC UNION ALL
# MAGIC SELECT 'gold_fact_sales', COUNT(*) FROM retail.gold.fact_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS retail.monitoring;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS retail.monitoring.pipeline_quality (
# MAGIC     checked_at TIMESTAMP,
# MAGIC     bronze_sales BIGINT,
# MAGIC     silver_sales BIGINT,
# MAGIC     quarantine_sales BIGINT,
# MAGIC     gold_sales BIGINT,
# MAGIC     rejection_rate DOUBLE,
# MAGIC     duplicated_sales BIGINT
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC INSERT INTO retail.monitoring.pipeline_quality
# MAGIC
# MAGIC WITH metrics AS (
# MAGIC     SELECT
# MAGIC         (SELECT COUNT(*) FROM retail.bronze.sales_auto) AS bronze_sales,
# MAGIC         (SELECT COUNT(*) FROM retail.silver.sales) AS silver_sales,
# MAGIC         (SELECT COUNT(*) FROM retail.silver.sales_quarantine) AS quarantine_sales,
# MAGIC         (SELECT COUNT(*) FROM retail.gold.fact_sales) AS gold_sales,
# MAGIC
# MAGIC         (
# MAGIC             SELECT COUNT(*)
# MAGIC             FROM (
# MAGIC                 SELECT sale_id
# MAGIC                 FROM retail.gold.fact_sales
# MAGIC                 GROUP BY sale_id
# MAGIC                 HAVING COUNT(*) > 1
# MAGIC             )
# MAGIC         ) AS duplicated_sales
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     current_timestamp() AS checked_at,
# MAGIC     bronze_sales,
# MAGIC     silver_sales,
# MAGIC     quarantine_sales,
# MAGIC     gold_sales,
# MAGIC
# MAGIC     ROUND(
# MAGIC         try_divide(
# MAGIC             quarantine_sales * 100.0,
# MAGIC             silver_sales + quarantine_sales
# MAGIC         ),
# MAGIC         4
# MAGIC     ) AS rejection_rate,
# MAGIC
# MAGIC     duplicated_sales
# MAGIC
# MAGIC FROM metrics;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail.monitoring.pipeline_quality
# MAGIC ORDER BY checked_at DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     sale_id,
# MAGIC     COUNT(*) AS occurrences
# MAGIC FROM retail.gold.fact_sales
# MAGIC GROUP BY sale_id
# MAGIC HAVING COUNT(*) > 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail.bronze.sales_auto
# MAGIC WHERE sale_id = 300001;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail.silver.sales
# MAGIC WHERE sale_id = 300001;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     sale_id,
# MAGIC     customer_id,
# MAGIC     product_id,
# MAGIC     store_id,
# MAGIC     validation_error
# MAGIC FROM retail.silver.sales_quarantine
# MAGIC WHERE sale_id = 300001;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail.gold.fact_sales
# MAGIC WHERE sale_id = 300001;