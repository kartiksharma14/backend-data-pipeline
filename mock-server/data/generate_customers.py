import json
from datetime import datetime, date
import random

first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Emma", "Liam", "Olivia"]
last_names = ["Doe", "Smith", "Brown", "Johnson", "Taylor", "Anderson"]

customers = []

for i in range(1, 21):
    first = random.choice(first_names)
    last = random.choice(last_names)
    customers.append({
        "customer_id": f"cust_{i:03}",
        "first_name": first,
        "last_name": last,
        "email": f"{first.lower()}.{last.lower()}{i}@example.com",
        "phone": f"+1{random.randint(1000000000, 9999999999)}",
        "address": f"{random.randint(1,999)} Main St, USA",
        "date_of_birth": str(date(1980 + i % 20, 1 + i % 12, 1 + i % 28)),
        "account_balance": round(random.uniform(100, 5000), 2),
        "created_at": datetime.utcnow().isoformat()
    })

with open("customers.json", "w") as f:
    json.dump(customers, f, indent=2)
