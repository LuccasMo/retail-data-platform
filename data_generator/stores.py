import csv
from pathlib import Path

STORES = [
    {
        "store_name": "Nexus Fortaleza Centro",
        "city": "Fortaleza",
        "state": "CE",
        "region": "Nordeste"
    },
    {
        "store_name": "Nexus Fortaleza Sul",
        "city": "Fortaleza",
        "state": "CE",
        "region": "Nordeste",
    },
    {
        "store_name": "Nexus Recife Centro",
        "city": "Recife",
        "state": "PE",
        "region": "Nordeste",
    },
    {
        "store_name": "Nexus Salvador Shopping",
        "city": "Salvador",
        "state": "BA",
        "region": "Nordeste",
    },
    {
        "store_name": "Nexus São Paulo Paulista",
        "city": "São Paulo",
        "state": "SP",
        "region": "Sudeste",
    },
    {
        "store_name": "Nexus São Paulo Norte",
        "city": "São Paulo",
        "state": "SP",
        "region": "Sudeste",
    },
    {
        "store_name": "Nexus Rio de Janeiro Centro",
        "city": "Rio de Janeiro",
        "state": "RJ",
        "region": "Sudeste",
    },
    {
        "store_name": "Nexus Belo Horizonte",
        "city": "Belo Horizonte",
        "state": "MG",
        "region": "Sudeste",
    },
    {
        "store_name": "Nexus Curitiba",
        "city": "Curitiba",
        "state": "PR",
        "region": "Sul",
    },
    {
        "store_name": "Nexus Porto Alegre",
        "city": "Porto Alegre",
        "state": "RS",
        "region": "Sul",
    },
    {
        "store_name": "Nexus Brasília",
        "city": "Brasília",
        "state": "DF",
        "region": "Centro-Oeste",
    },
    {
        "store_name": "Nexus Manaus",
        "city": "Manaus",
        "state": "AM",
        "region": "Norte",
    },

]

def generate_stores():
    output_path = Path("data/stores")
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / "stores.csv"

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow([
            "store_id",
            "store_name",
            "city",
            "state",
            "region"
        ])

        for store_id, store in enumerate(STORES, start=1):
            writer.writerow([
                store_id,
                store["store_name"],
                store["city"],
                store["state"],
                store["region"]
            ])

    print(f"{len(STORES)} Lojas geradas em {file_path}")


if __name__ == "__main__":
    generate_stores()