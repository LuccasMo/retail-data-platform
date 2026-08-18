import csv
from psycopg2.extras import execute_values
from database.connection import get_connection


def load_customers(cursor):
    with open("data/customers/customers.csv", "r", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    values = [
        (
            row["customer_id"],
            row["name"],
            row["email"],
            row["city"],
            row["state"],
            row["created_at"],
        )
        for row in rows
    ]

    execute_values(
        cursor,
        """
        INSERT INTO customers (
            customer_id,
            name,
            email,
            city,
            state,
            created_at
        )
        VALUES %s
        ON CONFLICT (customer_id) DO NOTHING;
        """,
        values,
    )


def load_products(cursor):
    with open("data/products/products.csv", "r", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    values = [
        (
            row["product_id"],
            row["product_name"],
            row["category"],
            row["brand"],
            row["cost"],
            row["price"],
            row["created_at"]
        )
        for row in rows
    ]

    execute_values(
        cursor,
        """
        INSERT INTO products (
            product_id,
            product_name,
            category,
            brand,
            cost,
            price,
            created_at
        )
        VALUES %s
        ON CONFLICT (product_id) DO NOTHING;
        """,
        values
    )


def load_stores(cursor):
    with open("data/stores/stores.csv", "r", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

        values = [
            (
                row["store_id"],
                row["store_name"],
                row["city"],
                row["state"],
                row["region"],
            )
            for row in rows
        ]

        execute_values(
            cursor,
            """
            INSERT INTO stores (
            store_id,
            store_name,
            city,
            state,
            region
        )
        VALUES %s
        ON CONFLICT (store_id) DO NOTHING;
        """,
        values
    )


def load_sales(cursor):
    with open("data/sales/sales.csv", "r", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

        values = [
            (
                row["sale_id"],
                row["customer_id"],
                row["product_id"],
                row["store_id"],
                row["quantity"],
                row["unit_price"],
                row["discount"],
                row["payment_method"],
                row["sale_timestamp"],
            )
            for row in rows
        ]

        execute_values(
            cursor,
            """
            INSERT INTO sales (
                sale_id,
                customer_id,
                product_id,
                store_id,
                quantity,
                unit_price,
                discount,
                payment_method,
                sale_timestamp
            )
            VALUES %s
            ON CONFLICT (sale_id) DO NOTHING;
            """,
            values
        )

def load_all_data():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            load_customers(cursor)
            print("Customers carregados.")

            load_products(cursor)
            print("Products carregados.")

            load_stores(cursor)
            print("Stores carregadas.")

            load_sales(cursor)
            print("Sales carregadas.")

        connection.commit()

        print("Carga concluída com sucesso!")

    except Exception as error:
        connection.rollback()

        print("Erro durante a carga.")
        print(error)

        raise

    finally:
        connection.close()


if __name__ == "__main__":
    load_all_data()