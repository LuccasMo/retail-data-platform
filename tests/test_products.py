import csv
from pathlib import Path

from data_generator.products import generate_products

def test_generate_products():
    generate_products(10)

    file_path = Path("data/products/products.csv")

    assert file_path.exists()

    with open(file_path, mode='r', encoding='utf-8') as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 10

    assert "product_id" in rows[0]
    assert "category" in rows[0]
    assert "brand" in rows[0]
    assert "cost" in rows[0]
    assert "price" in rows[0]
    

def test_product_price_is_greater_than_cost():
    generate_products(100)

    file_path = Path("data/products/products.csv")

    with open(file_path, "r", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    for row in rows:
        cost = float(row["cost"])
        price = float(row["price"])

        assert price > cost
