from flask import Blueprint, jsonify, request
from .db import db

customers_bp = Blueprint("customers", __name__)

@customers_bp.route("/", methods=["GET"])
def get_customers():
    query = "MATCH (c:Customer) RETURN c"
    result = db.query(query)
    customers = [record["c"]._properties for record in result]
    return jsonify(customers), 200


@customers_bp.route("/", methods=["POST"])
def create_customer():
    data = request.get_json()
    
    if not all(field in data for field in ["name", "age", "address"]):
        return jsonify({"message": "missing required fields"}), 400

    query = """
    CREATE (c:Customer {id: $id, name: $name, age: $age, address: $address})
    RETURN c
    """

    customer_id = len(db.query("MATCH (c:Customer) RETURN c")) + 1

    parameters = {
        "id": customer_id,
        "name": data["name"],
        "age": data["age"],
        "address": data["address"]
    }

    result = db.query(query, parameters)
    new_customer = result[0]["c"]._properties
    return jsonify(new_customer), 201


@customers_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    data = request.get_json()
    
    customer_query = "MATCH (c:Customer {id: $id}) RETURN c"
    customer_result = db.query(customer_query, {"id": customer_id})
    if not customer_result:
        return jsonify({"message": "customer not found"}), 404

    update_query = """
    MATCH (c:Customer {id: $id})
    SET c.name = $name, c.age = $age, c.address = $address
    RETURN c
    """

    parameters = {
        "id": customer_id,
        "name": data.get("name", customer_result[0]["c"]["name"]),
        "age": data.get("age", customer_result[0]["c"]["age"]),
        "address": data.get("address", customer_result[0]["c"]["address"])
    }

    result = db.query(update_query, parameters)
    updated_customer = result[0]["c"]._properties
    return jsonify(updated_customer), 200


@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):    
    customer_query = "MATCH (c:Customer {id: $id}) RETURN c"
    customer_result = db.query(customer_query, {"id": customer_id})
    if not customer_result:
        return jsonify({"message": "customer not found"}), 404
    
    delete_query = "MATCH (c:Customer {id: $id}) DELETE c"
    db.query(delete_query, {"id": customer_id})
    return jsonify({"message": "customer deleted"}), 200
