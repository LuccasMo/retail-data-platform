import csv
from pathlib import Path
from faker import Faker
import random

fake = Faker("pt-BR")

BRAZIL_STATES = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF",
    "ES", "GO", "MA", "MT", "MS", "MG", "PA",
    "PB", "PR", "PE", "PI", "RJ", "RN", "RS",
    "RO", "RR", "SC", "SP", "SE", "TO"
]

state = random.choice(BRAZIL_STATES)

output_path = Path("data/customers")
output_path.mkdir(parents=True, exist_ok=True)

file_path = output_path /"customers_02.csv"

with open (file_path, "w", newline="", encoding="utf-8)") as file:
    writer = csv.writer(file)

    writer.writerow([
        "customer_id",
        "name",
        "email",
        "city",
        "state",
        "created_at",
    ])

    for customer_id in range(10101, 10200):
        writer.writerow([
            customer_id,
            fake.name(),
            fake.email(),
            fake.city(),
            state,
            fake.date_time_this_year(),
        ])

print(f"Arquivo incremental criado em {file_path}")