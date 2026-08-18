from faker import Faker
import csv
from pathlib import Path
import random

BRAZIL_STATES = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF",
    "ES", "GO", "MA", "MT", "MS", "MG", "PA",
    "PB", "PR", "PE", "PI", "RJ", "RN", "RS",
    "RO", "RR", "SC", "SP", "SE", "TO"
]

fake = Faker("pt_BR")
state = random.choice(BRAZIL_STATES)


def generate_customers(quantity=100):
    output_path = Path("data/customers")

    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / "customers.csv"

    with open(file_path, mode='w', newline='', encoding= 'utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            "customer_id",
            "name",
            "email",
            "city",
            "state",
            "created_at"
        ])

        for customer_id in range(1, quantity + 1):
            writer.writerow([
                customer_id,
                fake.name(),
                fake.email(),
                fake.city(),
                state,
                fake.date_this_year()
            ])

    print(f"{quantity} clientes gerados em {file_path}")

if __name__ == "__main__":
    generate_customers(10000)