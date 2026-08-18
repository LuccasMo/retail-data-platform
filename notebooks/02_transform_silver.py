# Databricks notebook source
# Retail Data Platform
# Notebook: 02_transform_silver
# Objetivo: realizar validação e padronização dos dados para ingestão na camada Gold


df_customers = spark.table("retail.bronze.customers_auto")

display(df_customers)

# COMMAND ----------

df_customers.printSchema()

# COMMAND ----------

print(df_customers.columns)


# COMMAND ----------

df_customers = spark.table("retail.bronze.customers_auto")

print(df_customers.columns)


# COMMAND ----------

# MAGIC %md
# MAGIC **Saving silver customers**

# COMMAND ----------

from pyspark.sql import functions as F

df_customers = spark.table("retail.bronze.customers_auto")

print(df_customers.columns)
df_customers.printSchema()

# COMMAND ----------

df_customers_clean = (
    df_customers
    .select(
        F.col("customer_id").cast("int").alias("customer_id"),
        F.trim(F.col("name")).alias("name"),
        F.lower(F.trim(F.col("email"))).alias("email"),
        F.trim(F.col("city")).alias("city"),
        F.upper(F.trim(F.col("state"))).alias("state"),
        F.to_date(F.col("created_at")).alias("created_at")
    )
    .dropDuplicates(["customer_id"])
)

# COMMAND ----------

valid_condition = (
    F.col("customer_id").isNotNull()
    & F.col("name").isNotNull()
    & F.col("email").isNotNull()
    & F.col("state").rlike("^[A-Z]{2}$")
)

# COMMAND ----------

df_customers_valid = df_customers_clean.filter(valid_condition)

df_customers_invalid = df_customers_clean.filter(~valid_condition)

# COMMAND ----------

df_customers_valid.show(5)

# COMMAND ----------

print(df_customers_valid.columns)

# COMMAND ----------

(
    df_customers_valid.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.silver.customers")
)

# COMMAND ----------

(
    df_customers_invalid.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.silver.customers_quarantine")
)

# COMMAND ----------

# MAGIC %md
# MAGIC **Saving silver products**
# MAGIC

# COMMAND ----------

from pyspark.sql import functions as F

df_products = spark.table("retail.bronze.products_auto")

df_products_clean = (
    df_products
    .select(
        F.col("product_id").cast("int").alias("product_id"),
        F.trim(F.col("product_name")).alias("product_name"),
        F.trim(F.col("category")).alias("category"),
        F.trim(F.col("brand")).alias("brand"),
        F.col("cost").cast("double").alias("cost"),
        F.col("price").cast("double").alias("price"),
        F.to_date(F.col("created_at")).alias("created_at"),
    )
    .dropDuplicates(["product_id"])
)

products_valid_condition = (
    F.col("product_id").isNotNull()
    & F.col("product_name").isNotNull()
    & (F.length(F.col("product_name")) > 0)
    & F.col("category").isNotNull()
    & F.col("brand").isNotNull()
    & F.col("cost").isNotNull()
    & F.col("price").isNotNull()
    & (F.col("cost") > 0)
    & (F.col("price") > F.col("cost"))
)

df_products_valid = (
    df_products_clean
    .filter(products_valid_condition)
)

df_products_invalid = (
    df_products_clean
    .filter(~products_valid_condition)
)

(
    df_products_valid.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.silver.products")
)

(
    df_products_invalid.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.silver.products_quarantine")
)

# COMMAND ----------

df_stores = spark.table("retail.bronze.stores_auto")

df_stores_clean = (
    df_stores
    .select(
        F.col("store_id").cast("int").alias("store_id"),
        F.trim(F.col("store_name")).alias("store_name"),
        F.trim(F.col("city")).alias("city"),
        F.upper(F.trim(F.col("state"))).alias("state"),
        F.trim(F.col("region")).alias("region"),
    )
    .dropDuplicates(["store_id"])
)

valid_regions = [
    "Norte",
    "Nordeste",
    "Centro-Oeste",
    "Sudeste",
    "Sul",
]

stores_valid_condition = (
    F.col("store_id").isNotNull()
    & F.col("store_name").isNotNull()
    & (F.length(F.col("store_name")) > 0)
    & F.col("city").isNotNull()
    & (F.length(F.col("city")) > 0)
    & F.col("state").rlike("^[A-Z]{2}$")
    & F.col("region").isin(valid_regions)
)

df_stores_valid = (
    df_stores_clean
    .filter(stores_valid_condition)
)

df_stores_invalid = (
    df_stores_clean
    .filter(~stores_valid_condition)
)

(
    df_stores_valid.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.silver.stores")
)

(
    df_stores_invalid.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.silver.stores_quarantine")
)

# COMMAND ----------

df_sales = spark.table("retail.bronze.sales_auto")

df_sales_clean = (
    df_sales
    .select(
        F.col("sale_id").cast("int").alias("sale_id"),
        F.col("customer_id").cast("int").alias("customer_id"),
        F.col("product_id").cast("int").alias("product_id"),
        F.col("store_id").cast("int").alias("store_id"),
        F.col("quantity").cast("int").alias("quantity"),
        F.col("unit_price").cast("double").alias("unit_price"),
        F.col("discount").cast("double").alias("discount"),
        F.trim(F.col("payment_method")).alias("payment_method"),
        F.to_timestamp(F.col("sale_timestamp")).alias("sale_timestamp"),
    )
    .dropDuplicates(["sale_id"])
)

# COMMAND ----------

df_valid_customers = (
    spark.table("retail.silver.customers")
    .select("customer_id")
    .withColumnRenamed("customer_id", "valid_customer_id")
)

df_valid_products = (
    spark.table("retail.silver.products")
    .select("product_id")
    .withColumnRenamed("product_id", "valid_product_id")
)

df_valid_stores = (
    spark.table("retail.silver.stores")
    .select("store_id")
    .withColumnRenamed("store_id", "valid_store_id")
)

# COMMAND ----------

df_sales_validated = (
    df_sales_clean
    .join(
        df_valid_customers,
        df_sales_clean.customer_id == df_valid_customers.valid_customer_id,
        "left"
    )
    .join(
        df_valid_products,
        df_sales_clean.product_id == df_valid_products.valid_product_id,
        "left"
    )
    .join(
        df_valid_stores,
        df_sales_clean.store_id == df_valid_stores.valid_store_id,
        "left"
    )
)

# COMMAND ----------

df_sales_validated = (
    df_sales_validated
    .withColumn(
        "validation_error",
        F.when(
            F.col("sale_id").isNull(),
            "INVALID_SALE_ID"
        )
        .when(
            F.col("customer_id").isNull(),
            "INVALID_CUSTOMER_ID"
        )
        .when(
            F.col("valid_customer_id").isNull(),
            "CUSTOMER_NOT_FOUND"
        )
        .when(
            F.col("product_id").isNull(),
            "INVALID_PRODUCT_ID"
        )
        .when(
            F.col("valid_product_id").isNull(),
            "PRODUCT_NOT_FOUND"
        )
        .when(
            F.col("store_id").isNull(),
            "INVALID_STORE_ID"
        )
        .when(
            F.col("valid_store_id").isNull(),
            "STORE_NOT_FOUND"
        )
        .when(
            F.col("quantity").isNull() | (F.col("quantity") <= 0),
            "INVALID_QUANTITY"
        )
        .when(
            F.col("unit_price").isNull() | (F.col("unit_price") <= 0),
            "INVALID_UNIT_PRICE"
        )
        .when(
            F.col("discount").isNull() | (F.col("discount") < 0),
            "INVALID_DISCOUNT"
        )
        .when(
            F.col("sale_timestamp").isNull(),
            "INVALID_TIMESTAMP"
        )
    )
)

# COMMAND ----------

df_sales_valid = (
    df_sales_validated
    .filter(F.col("validation_error").isNull())
    .drop(
        "valid_customer_id",
        "valid_product_id",
        "valid_store_id",
        "validation_error"
    )
)

# COMMAND ----------

df_sales_invalid = (
    df_sales_validated
    .filter(F.col("validation_error").isNotNull())
    .drop(
        "valid_customer_id",
        "valid_product_id",
        "valid_store_id"
    )
)

# COMMAND ----------

valid_payment_methods = [
    "Pix",
    "Cartão de Crédito",
    "Cartão de Débito",
    "Dinheiro",
    "Boleto",
]

sales_business_condition = (
    F.col("sale_id").isNotNull()
    & F.col("customer_id").isNotNull()
    & F.col("product_id").isNotNull()
    & F.col("store_id").isNotNull()
    & F.col("quantity").isNotNull()
    & (F.col("quantity") > 0)
    & F.col("unit_price").isNotNull()
    & (F.col("unit_price") > 0)
    & F.col("discount").isNotNull()
    & (F.col("discount") >= 0)
    & (F.col("discount") <= F.col("unit_price") * F.col("quantity"))
    & F.col("payment_method").isin(valid_payment_methods)
    & F.col("sale_timestamp").isNotNull()
)

# COMMAND ----------

df_sales_business_valid = (
    df_sales_clean
    .filter(sales_business_condition)
)

df_sales_business_invalid = (
    df_sales_clean
    .filter(~sales_business_condition)
)

# COMMAND ----------

df_valid_customers = (
    spark.table("retail.silver.customers")
    .select("customer_id")
)

df_valid_products = (
    spark.table("retail.silver.products")
    .select("product_id")
)

df_valid_stores = (
    spark.table("retail.silver.stores")
    .select("store_id")
)

# COMMAND ----------

df_sales_with_refs = (
    df_sales_business_valid
    .join(
        df_valid_customers.withColumnRenamed(
            "customer_id",
            "valid_customer_id"
        ),
        df_sales_business_valid.customer_id == F.col("valid_customer_id"),
        "left"
    )
    .join(
        df_valid_products.withColumnRenamed(
            "product_id",
            "valid_product_id"
        ),
        df_sales_business_valid.product_id == F.col("valid_product_id"),
        "left"
    )
    .join(
        df_valid_stores.withColumnRenamed(
            "store_id",
            "valid_store_id"
        ),
        df_sales_business_valid.store_id == F.col("valid_store_id"),
        "left"
    )
)

# COMMAND ----------

(
    df_sales_valid.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("retail.silver.sales")
)

(
    df_sales_invalid.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("retail.silver.sales_quarantine")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM retail.silver.customers;
# MAGIC SELECT COUNT(*) FROM retail.silver.customers_quarantine;
# MAGIC
# MAGIC SELECT COUNT(*) FROM retail.silver.products;
# MAGIC SELECT COUNT(*) FROM retail.silver.products_quarantine;
# MAGIC
# MAGIC SELECT COUNT(*) FROM retail.silver.stores;
# MAGIC SELECT COUNT(*) FROM retail.silver.stores_quarantine;
# MAGIC
# MAGIC SELECT COUNT(*) FROM retail.silver.sales;
# MAGIC SELECT COUNT(*) FROM retail.silver.sales_quarantine;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'customers' AS tabela, COUNT(*) AS registros
# MAGIC FROM retail.silver.customers
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'customers_quarantine', COUNT(*)
# MAGIC FROM retail.silver.customers_quarantine
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'products', COUNT(*)
# MAGIC FROM retail.silver.products
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'products_quarantine', COUNT(*)
# MAGIC FROM retail.silver.products_quarantine
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'stores', COUNT(*)
# MAGIC FROM retail.silver.stores
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'stores_quarantine', COUNT(*)
# MAGIC FROM retail.silver.stores_quarantine
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'sales', COUNT(*)
# MAGIC FROM retail.silver.sales
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 'sales_quarantine', COUNT(*)
# MAGIC FROM retail.silver.sales_quarantine;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     sale_id,
# MAGIC     customer_id,
# MAGIC     product_id,
# MAGIC     store_id,
# MAGIC     quantity,
# MAGIC     unit_price,
# MAGIC     validation_error
# MAGIC FROM retail.silver.sales_quarantine
# MAGIC WHERE sale_id BETWEEN 200001 AND 200006
# MAGIC ORDER BY sale_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail.silver.sales
# MAGIC WHERE sale_id = 200006;