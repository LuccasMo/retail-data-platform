# Databricks notebook source
# Retail Data Platform
# Notebook: 01_ingest_bronze
# Objetivo: realizar ingestão incremental da Landing para a camada Bronze
# usando Auto Loader, checkpoints independentes e Delta Lake.

df_customers = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(
        "abfss://landing@stretaildatalake1231.dfs.core.windows.net/customers/customers.csv"
    )
)

display(df_customers)

# COMMAND ----------


df_products = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(
        "abfss://landing@stretaildatalake1231.dfs.core.windows.net/products/products.csv"
    )
)

display(df_products)

# COMMAND ----------


df_stores = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(
        "abfss://landing@stretaildatalake1231.dfs.core.windows.net/stores/stores.csv"
    )
)

display(df_stores)

# COMMAND ----------


df_sales = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(
        "abfss://landing@stretaildatalake1231.dfs.core.windows.net/sales/sales.csv"
    )
)

display(df_sales)

# COMMAND ----------

df_customers.printSchema()

# COMMAND ----------

df_products.printSchema()

# COMMAND ----------

df_stores.printSchema()

# COMMAND ----------

df_sales.printSchema()

# COMMAND ----------


df_customers.count()

# COMMAND ----------

df_products.count()

# COMMAND ----------

df_stores.count()

# COMMAND ----------

df_sales.count()

# COMMAND ----------

(
    df_customers.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.bronze.customers")
)
(
    df_products.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.bronze.products")
) 
(
    df_stores.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.bronze.stores")
) 
(
    df_sales.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.bronze.sales")
) 

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM retail.bronze.customers
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM retail.bronze.products
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM retail.bronze.stores
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM retail.bronze.sales
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC Defining customers schema and checkpoint

# COMMAND ----------

storage_account = "stretaildatalake1231"

base_path = (
    f"abfss://landing@{storage_account}.dfs.core.windows.net"
)

customers_path = f"{base_path}/customers"
products_path = f"{base_path}/products"
stores_path = f"{base_path}/stores"
sales_path = f"{base_path}/sales"


customers_schema_path = (
    f"{base_path}/_checkpoints/customers/schema_v9/"
)

products_schema_path = (
    f"{base_path}/_checkpoints/products/schema_v9/"
)

stores_schema_path = (
    f"{base_path}/_checkpoints/stores/schema_v9/"
)

sales_schema_path = (
    f"{base_path}/_checkpoints/sales/schema_v9/"
)

# COMMAND ----------

customers_checkpoint_path = (
    f"{base_path}/_checkpoints/customers/checkpoint_v9/"
)

products_checkpoint_path = (
    f"{base_path}/_checkpoints/products/heckpoint_v9/"
)

stores_checkpoint_path = (
    f"{base_path}/_checkpoints/stores/heckpoint_v9/"
)

sales_checkpoint_path = (
    f"{base_path}/_checkpoints/sales/heckpoint_v9/"
)

# COMMAND ----------

df_customers_stream = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("header", "true")
    .option("cloudFiles.inferColumnTypes", "true")
    .option("cloudFiles.schemaLocation", customers_path)
    .load(customers_path)
)

print(df_customers_stream.isStreaming)

# COMMAND ----------

df_products_stream = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("header", "true")
    .option("cloudFiles.inferColumnTypes", "true")
    .option(
        "cloudFiles.schemaLocation",
        products_schema_path
    )
    .load(products_path)
)

# COMMAND ----------

df_stores_stream = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("header", "true")
    .option("cloudFiles.inferColumnTypes", "true")
    .option(
        "cloudFiles.schemaLocation",
        stores_schema_path
    )
    .load(stores_path)
)

# COMMAND ----------

df_sales_stream = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("header", "true")
    .option("cloudFiles.inferColumnTypes", "true")
    .option(
        "cloudFiles.schemaLocation",
        sales_schema_path
    )
    .load(sales_path)
)

# COMMAND ----------

query_customers = (
    df_customers_stream.writeStream
    .format("delta")
    .option(
        "checkpointLocation",
        customers_checkpoint_path
    )
    .trigger(availableNow=True)
    .toTable("retail.bronze.customers_auto")
)

# COMMAND ----------

query_products = (
    df_products_stream.writeStream
    .format("delta")
    .option(
        "checkpointLocation",
        products_checkpoint_path
    )
    .trigger(availableNow=True)
    .toTable("retail.bronze.products_auto")
)

# COMMAND ----------

query_stores = (
    df_stores_stream.writeStream
    .format("delta")
    .option(
        "checkpointLocation",
        stores_checkpoint_path
    )
    .trigger(availableNow=True)
    .toTable("retail.bronze.stores_auto")
)

# COMMAND ----------

query_sales = (
    df_sales_stream.writeStream
    .format("delta")
    .option(
        "checkpointLocation",
        sales_checkpoint_path
    )
    .trigger(availableNow=True)
    .toTable("retail.bronze.sales_auto")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail.bronze.sales_auto
# MAGIC WHERE sale_id BETWEEN 200001 AND 200006
# MAGIC ORDER BY sale_id;

# COMMAND ----------

df_test = spark.table("retail.bronze.customers_auto")

print(df_test.columns)