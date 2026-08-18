# Databricks notebook source
# Retail Data Platform
# Notebook: 03_build_gold
# Objetivo: receber dados validados da camada silver após validações
# para serem consumidos

from pyspark.sql import functions as F

df_customers = spark.table("retail.silver.customers")
df_products = spark.table("retail.silver.products")
df_stores = spark.table("retail.silver.stores")
df_sales = spark.table("retail.silver.sales")

# COMMAND ----------

df_dim_customers = (
    df_customers
    .select(
        "customer_id",
        "name",
        "email",
        "city",
        "state",
        "created_at"
    )
)

# COMMAND ----------

(
    df_dim_customers.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.gold.dim_customers")
)

# COMMAND ----------

df_dim_products = (
    df_products
    .select(
        "product_id",
        "product_name",
        "category",
        "brand",
        "cost",
        "price"
    )
)

# COMMAND ----------

(
    df_dim_products.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.gold.dim_products")
)

# COMMAND ----------

df_dim_stores = (
    df_stores
    .select(
        "store_id",
        "store_name",
        "city",
        "state",
        "region"
    )
)

# COMMAND ----------

(
    df_dim_stores.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.gold.dim_stores")
)

# COMMAND ----------

df_dim_date = (
    df_sales
    .select(
        F.to_date("sale_timestamp").alias("date")
    )
    .distinct()
    .withColumn(
        "date_id",
        F.date_format("date", "yyyyMMdd").cast("int")
    )
    .withColumn("year", F.year("date"))
    .withColumn("month", F.month("date"))
    .withColumn("day", F.dayofmonth("date"))
    .withColumn("quarter", F.quarter("date"))
    .withColumn("day_of_week", F.dayofweek("date"))
    .withColumn("month_name", F.date_format("date", "MMMM"))
)

# COMMAND ----------

(
    df_dim_date.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.gold.dim_date")
)

# COMMAND ----------

df_fact_sales = (
    df_sales
    .withColumn(
        "gross_amount",
        F.col("quantity") * F.col("unit_price")
    )
    .withColumn(
        "net_amount",
        F.col("gross_amount") - F.col("discount")
    )
    .withColumn(
        "date_id",
        F.date_format("sale_timestamp", "yyyyMMdd").cast("int")
    )
)

# COMMAND ----------

df_products_cost = (
    df_products
    .select(
        "product_id",
        "cost"
    )
)

# COMMAND ----------

df_fact_sales = (
    df_fact_sales
    .join(
        df_products_cost,
        on="product_id",
        how="left"
    )
)

# COMMAND ----------

df_fact_sales = (
    df_fact_sales
    .withColumn(
        "total_cost",
        F.col("quantity") * F.col("cost")
    )
    .withColumn(
        "profit",
        F.col("net_amount") - F.col("total_cost")
    )
)

# COMMAND ----------

df_fact_sales = (
    df_fact_sales
    .select(
        "sale_id",
        "customer_id",
        "product_id",
        "store_id",
        "date_id",
        "quantity",
        "unit_price",
        "discount",
        "gross_amount",
        "net_amount",
        "total_cost",
        "profit",
        "payment_method",
        "sale_timestamp"
    )
)

# COMMAND ----------

(
    df_fact_sales.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.gold.fact_sales")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     SUM(net_amount) AS revenue
# MAGIC FROM retail.gold.fact_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     SUM(profit) AS profit
# MAGIC FROM retail.gold.fact_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     AVG(net_amount) AS average_ticket
# MAGIC FROM retail.gold.fact_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     st.region,
# MAGIC     SUM(f.net_amount) AS revenue
# MAGIC FROM retail.gold.fact_sales f
# MAGIC
# MAGIC JOIN retail.gold.dim_stores st
# MAGIC     ON f.store_id = st.store_id
# MAGIC
# MAGIC GROUP BY st.region
# MAGIC
# MAGIC ORDER BY revenue DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     p.product_name,
# MAGIC     SUM(f.quantity) AS units_sold,
# MAGIC     SUM(f.net_amount) AS revenue
# MAGIC FROM retail.gold.fact_sales f
# MAGIC
# MAGIC JOIN retail.gold.dim_products p
# MAGIC     ON f.product_id = p.product_id
# MAGIC
# MAGIC GROUP BY p.product_name
# MAGIC
# MAGIC ORDER BY revenue DESC
# MAGIC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC Sales_daily
# MAGIC

# COMMAND ----------

df_sales_daily = (
    df_fact_sales
    .groupBy("date_id")
    .agg(
        F.sum("net_amount").alias("revenue"),
        F.sum("profit").alias("profit"),
        F.sum("quantity").alias("unit_solt"),
        F.countDistinct("customer_id").alias("oders"),
        F.avg("net_amount").alias("avarage_ticket")
    )
)

(
    df_sales_daily.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.gold.sale_daily")
)

# COMMAND ----------

# MAGIC %md
# MAGIC Product_performance

# COMMAND ----------

df_product_performance = (
    df_fact_sales
    .groupBy("product_id")
    .agg(
        F.sum("quantity").alias("units_sold"),
        F.sum("net_amount").alias("revenue"),
        F.sum("profit").alias("profit"),
        F.countDistinct("sale_id").alias("orders")
    )
)

(
    df_product_performance.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.gold.product_performance")
)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC Store_performance

# COMMAND ----------

df_store_performance = (
    df_fact_sales
    .groupBy("store_id")
    .agg(
        F.sum("net_amount").alias("revenue"),
        F.sum("profit").alias("profit"),
        F.sum("quantity").alias("units_sold"),
        F.countDistinct("sale_id").alias("orders")
    )
)

(
    df_store_performance.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.gold.store_performance")
)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC Customer_360

# COMMAND ----------

df_customer_360 = (
    df_fact_sales
    .groupBy("customer_id")
    .agg(
        F.countDistinct("sale_id").alias("total_orders"),
        F.sum("net_amount").alias("total_spent"),
        F.avg("net_amount").alias("avarage_ticket"),
        F.max("sale_timestamp").alias("last_purchase")
    )
)

(
    df_customer_360.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.gold.customer_360")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM retail.gold.sale_daily LIMIT 10;
# MAGIC SELECT * FROM retail.gold.product_performance LIMIT 10;
# MAGIC SELECT * FROM retail.gold.store_performance LIMIT 10;
# MAGIC SELECT * FROM retail.gold.customer_360 LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT COUNT(*) AS bronze_sales
# MAGIC FROM retail.bronze.sales_auto;
# MAGIC
# MAGIC SELECT COUNT(*) AS silver_sales
# MAGIC FROM retail.silver.sales;
# MAGIC
# MAGIC SELECT COUNT(*) AS gold_sales
# MAGIC FROM retail.gold.fact_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     sale_id,
# MAGIC     COUNT(*) AS occurrences
# MAGIC FROM retail.gold.fact_sales
# MAGIC GROUP BY sale_id
# MAGIC HAVING COUNT(*) > 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT sale_id
# MAGIC FROM retail.gold.fact_sales
# MAGIC LIMIT 1;