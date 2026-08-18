import csv
from pathlib import Path
import random


STORES = [
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


outpath = Path("data/stores")
outpath.mkdir(parents=True, exist_ok=True)

file_path = outpath / "stores_02.csv"

with open(file_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow ([
        "store_id",
        "store_name",
        "city",
        "state",
        "region",
    ])

    for store_id, store in enumerate(STORES, start=13):
        writer.writerow ([
            store_id,
            store["store_name"],
            store["city"],
            store["state"],
            store["region"]
        ])

print(f"{len(STORES)} Lojas geradas em {file_path}")
        
