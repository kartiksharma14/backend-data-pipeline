from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models.customer import Customer
from services.ingestion import ingest_customers
import os
import time

app = FastAPI(title="Customer Pipeline API")

MOCK_API_URL = os.getenv("MOCK_API_URL")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    retries = 5
    while retries:
        try:
            Customer.metadata.create_all(bind=engine)
            break
        except Exception:
            retries -= 1
            time.sleep(3)
    if retries == 0:
        raise RuntimeError("Database not ready")

@app.post("/api/ingest")
def ingest(db: Session = Depends(get_db)):
    try:
        count = ingest_customers(db, MOCK_API_URL)
        return {"status": "success", "records_processed": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers", response_model=dict)
def list_customers(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    customers = db.query(Customer).offset(offset).limit(limit).all()
    total = db.query(Customer).count()

    return {
        "data": [customer_to_dict(c) for c in customers],
        "total": total,
        "page": page,
        "limit": limit
    }

@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter_by(customer_id=customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer_to_dict(customer)

@app.get("/api/health")
def health():
    return {"status": "ok"}

def customer_to_dict(customer):
    return {
        "customer_id": customer.customer_id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email,
        "phone": customer.phone,
        "address": customer.address,
        "date_of_birth": customer.date_of_birth.isoformat() if customer.date_of_birth else None,
        "account_balance": float(customer.account_balance) if customer.account_balance else None,
        "created_at": customer.created_at.isoformat() if customer.created_at else None,
    }
