from flask import Blueprint, jsonify, request

customers_bp = Blueprint("customers", __name__)

customers = [
    {"id": 1, "name": "Jonas", "age": "21", "address": "harkjedunomed"},
    {"id": 2, "name": "Ponas", "age": "21", "address": "harkjeduhellenomed"}
]

@customers_bp.route("/", methods=["GET"])
def get_customers():
    return jsonify(customers)


@customers_bp.route("/", methods=["POST"])
def create_customers():
    data = request.get_json()
    
    if not all(field in data for field in ["name", "age", "address"]):
        return jsonify({"message": "missing required fields"})

    new_customer = {
        "id": customers[-1]["id"] + 1 if customers else 1,
        "name": data["name"],
        "age": data["age"],
        "address": data["address"]
    }

    customers.append(new_customer)

    return jsonify(new_customer)


@customers_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customers(customer_id):
    data = request.get_json()
    
    customer = next((customer for customer in customers if customer["id"] == customer_id), None)

    if customer is None:
        return jsonify({"message", "customer not found"})

    customer["name"] = data.get("name", customer["name"])
    customer["age"] = data.get("age", customer["age"])
    customer["address"] = data.get("address", customer["address"])
    return jsonify(customers)


@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customers(customer_id):
    customer = next((customer for customer in customers if customer["id"] == customer_id), None)

    if customer == None:
        return jsonify({"message": "customer not found"})

    customers.remove(customer)

    return jsonify(customers)

