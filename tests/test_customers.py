import csv
from pathlib import Path

from data_generator.customers import generate_customers

def test_generate_customers():
    generate_customers(10)

    file_path = Path("data/customers/customers.csv")

    assert file_path.exists(), "O arquivo customers.csv nao foi criado."

    with open(file_path, mode='r', encoding='utf-8') as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 10
    assert "customer_id" in rows[0]
    assert "email" in rows[0]
    assert "state" in rows[0]