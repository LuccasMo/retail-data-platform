import csv
from pathlib import Path
import random
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

output_path = Path("data/products")
output_path.mkdir(parents=True, exist_ok=True)

file_path = output_path / "products_02.csv"

with open(file_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow ([
        "product_id",
        "product_name",
        "category",
        "brand",
        "cost",
        "price",
        "created_ad",
    ])

    for product_id in range (501, 600):
        cost = round(random.uniform(10, 1000), 2)
        margin = random.uniform(0.1, 0.5)
        price = round(cost * (1 + margin), 2)
        
        writer.writerow ([
            product_id,
            fake.catch_phrase(),
            random.choice(CATEGORIES),
            random.choice(BRANDS),
            cost,
            price,
            fake.date_time_this_year()
        ])

print(f"Arquivo incremental criado em {file_path}")