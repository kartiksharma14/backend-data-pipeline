from flask import Flask, jsonify, request, abort
import json
import os

app = Flask(__name__)

DATA_PATH = os.path.join("data", "customers.json")

def load_customers():
    with open(DATA_PATH, "r") as f:
        return json.load(f)

@app.route("/api/health", methods=["GET"])
def health():
    return {"status": "ok"}

@app.route("/api/customers", methods=["GET"])
def get_customers():
    customers = load_customers()

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    start = (page - 1) * limit
    end = start + limit

    return jsonify({
        "data": customers[start:end],
        "total": len(customers),
        "page": page,
        "limit": limit
    })

@app.route("/api/customers/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    customers = load_customers()
    customer = next((c for c in customers if c["customer_id"] == customer_id), None)

    if not customer:
        abort(404, description="Customer not found")

    return jsonify(customer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
