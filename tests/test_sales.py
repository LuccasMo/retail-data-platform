import csv
from pathlib import Path

from data_generator.sales import generate_sales


def test_generate_sales():
    generate_sales(50)

    file_path = Path("data/sales/sales.csv")

    assert file_path.exists()

    with open(file_path, "r", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 50

    assert "sale_id" in rows[0]
    assert "customer_id" in rows[0]
    assert "product_id" in rows[0]
    assert "store_id" in rows[0]
    assert "quantity" in rows[0]
    assert "unit_price" in rows[0]
    assert "discount" in rows[0]

def test_sales_references_exist():
    generate_sales(100)

    with open(
        "data/customers/customers.csv",
        "r",
        encoding="utf-8",
    ) as file:
        customers = list(csv.DictReader(file))

    with open(
        "data/products/products.csv",
        "r",
        encoding="utf-8",
    ) as file:
        products = list(csv.DictReader(file))

    with open(
        "data/stores/stores.csv",
        "r",
        encoding="utf-8",
    ) as file:
        stores = list(csv.DictReader(file))

    with open(
        "data/sales/sales.csv",
        "r",
        encoding="utf-8",
    ) as file:
        sales = list(csv.DictReader(file))

    customer_ids = {
        customer["customer_id"]
        for customer in customers
    }

    product_ids = {
        product["product_id"]
        for product in products
    }

    store_ids = {
        store["store_id"]
        for store in stores
    }

    for sale in sales:
        assert sale["customer_id"] in customer_ids
        assert sale["product_id"] in product_ids
        assert sale["store_id"] in store_ids

def test_sales_business_rules():
    generate_sales(100)

    with open(
        "data/sales/sales.csv",
        "r",
        encoding="utf-8",
    ) as file:
        sales = list(csv.DictReader(file))

    for sale in sales:
        quantity = int(sale["quantity"])
        unit_price = float(sale["unit_price"])
        discount = float(sale["discount"])

        assert quantity > 0
        assert unit_price > 0
        assert discount >= 0