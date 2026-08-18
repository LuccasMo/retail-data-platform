import csv
import random
from datetime import datetime
from pathlib import Path

from faker import Faker

fake = Faker("pt_BR")

CATEGORIES = [
    "Eletrônicos",
    "informática",
    "Celulares",
    "Eletrodomésticos",
    "Casa",
    "Esportes",
    "Moda",
    "Beleza"
]

BRANDS = [
    "Nexus",
    "TechPro",
    "SmartOne",
    "HomeTech",
    "Ultrafit",
    "PowerTech",
    "Connect"
]

def generate_products(quantity=100):
    output_path = Path("data/products")
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / "products.csv"

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            "product_id",
            "product_name",
            "category",
            "brand",
            "cost",
            "price",
            "created_at"
        ])

        for product_id in range(1, quantity + 1):
            cost = round(random.uniform(10, 1000), 2)
            margin = random.uniform(0.1, 0.5)
            price = round(cost * (1 + margin), 2)

            writer.writerow([
                product_id,
                fake.catch_phrase(),
                random.choice(CATEGORIES),
                random.choice(BRANDS),
                cost,
                price,
                fake.date_time_this_year(),
            ])

    print(f"{quantity} produtos gerados em {file_path}")

if __name__ == "__main__":
    generate_products(500)