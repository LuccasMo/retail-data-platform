import csv
from pathlib import Path

from data_generator.stores import generate_stores


def test_generate_stores():
    generate_stores()

    file_path = Path("data/stores/stores.csv")

    assert file_path.exists()

    with open(file_path, "r", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 12

    assert "store_id" in rows[0]
    assert "store_name" in rows[0]
    assert "city" in rows[0]
    assert "state" in rows[0]
    assert "region" in rows[0]