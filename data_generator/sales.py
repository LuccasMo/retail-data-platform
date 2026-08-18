import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


PAYMENT_METHODS = [
    "Pix",
    "Cartão de Crédito",
    "Cartão de Débito",
    "Dinheiro",
    "Boleto",
]


def load_csv(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def random_sale_datetime():
    start_date = datetime.now() - timedelta(days=365)
    random_days = random.randint(0, 365)
    random_seconds = random.randint(0, 86400)

    return start_date + timedelta(
        days=random_days,
        seconds=random_seconds,
    )


def generate_sales(quantity=1000):
    customers = load_csv("data/customers/customers.csv")
    products = load_csv("data/products/products.csv")
    stores = load_csv("data/stores/stores.csv")

    output_path = Path("data/sales")
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / "sales.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "sale_id",
            "customer_id",
            "product_id",
            "store_id",
            "quantity",
            "unit_price",
            "discount",
            "payment_method",
            "sale_timestamp",
        ])

        for sale_id in range(1, quantity + 1):
            customer = random.choice(customers)
            product = random.choice(products)
            store = random.choice(stores)

            unit_price = float(product["price"])
            quantity_sold = random.randint(1, 5)

            discount_percentage = random.choice([
                0,
                0,
                0,
                0.05,
                0.10,
                0.15,
            ])

            gross_value = unit_price * quantity_sold
            discount = round(gross_value * discount_percentage, 2)

            writer.writerow([
                sale_id,
                customer["customer_id"],
                product["product_id"],
                store["store_id"],
                quantity_sold,
                unit_price,
                discount,
                random.choice(PAYMENT_METHODS),
                random_sale_datetime(),
            ])

    print(f"{quantity} vendas geradas em {file_path}")


if __name__ == "__main__":
    generate_sales(100000)