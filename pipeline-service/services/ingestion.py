import requests
from sqlalchemy.orm import Session
from models.customer import Customer
from datetime import datetime, date

def normalize_customer(item: dict) -> dict:
    if isinstance(item.get("created_at"), str):
        item["created_at"] = datetime.fromisoformat(item["created_at"])

    if isinstance(item.get("date_of_birth"), str):
        item["date_of_birth"] = date.fromisoformat(item["date_of_birth"])

    return item


def ingest_customers(db: Session, base_url: str):
    page = 1
    limit = 10
    total_processed = 0

    while True:
        response = requests.get(
            f"{base_url}/api/customers",
            params={"page": page, "limit": limit},
            timeout=10
        )
        response.raise_for_status()
        payload = response.json()

        data = payload["data"]
        if not data:
            break

        for item in data:
            try:
                item = normalize_customer(item)
                customer = Customer(**item)
                db.merge(customer)
                total_processed += 1
            except Exception as e:
                print(f"Skipping record {item.get('customer_id')}: {e}")

        db.commit()

        if len(data) < limit:
            break

        page += 1

    return total_processed
