from flask import Blueprint, jsonify, request
from .db import db

employees_bp = Blueprint("employees", __name__)

@employees_bp.route("/", methods=["GET"])
def get_employees():
    query = "MATCH (e:Employee) RETURN e"
    result = db.query(query)
    employees = [record["e"]._properties for record in result]
    return jsonify(employees), 200


@employees_bp.route("/", methods=["POST"])
def create_employee():
    data = request.get_json()
    
    if not all(field in data for field in ["name", "address", "branch"]):
        return jsonify({"message": "missing required fields"}), 400

    query = """
    CREATE (e:Employee {id: $id, name: $name, address: $address, branch: $branch})
    RETURN e
    """

    employee_id = len(db.query("MATCH (e:Employee) RETURN e")) + 1

    parameters = {
        "id": employee_id,
        "name": data["name"],
        "address": data["address"],
        "branch": data["branch"]
    }

    result = db.query(query, parameters)
    new_employee = result[0]["e"]._properties
    return jsonify(new_employee), 201


@employees_bp.route("/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    data = request.get_json()
    
    employee_query = "MATCH (e:Employee {id: $id}) RETURN e"
    employee_result = db.query(employee_query, {"id": employee_id})
    if not employee_result:
        return jsonify({"message": "employee not found"}), 404

    update_query = """
    MATCH (e:Employee {id: $id})
    SET e.name = $name, e.address = $address, e.branch = $branch
    RETURN e
    """

    parameters = {
        "id": employee_id,
        "name": data.get("name", employee_result[0]["e"]["name"]),
        "address": data.get("address", employee_result[0]["e"]["address"]),
        "branch": data.get("branch", employee_result[0]["e"]["branch"])
    }

    result = db.query(update_query, parameters)
    updated_employee = result[0]["e"]._properties
    return jsonify(updated_employee), 200


@employees_bp.route("/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):    
    employee_query = "MATCH (e:Employee {id: $id}) RETURN e"
    employee_result = db.query(employee_query, {"id": employee_id})
    if not employee_result:
        return jsonify({"message": "employee not found"}), 404
    
    delete_query = "MATCH (e:Employee {id: $id}) DELETE e"
    db.query(delete_query, {"id": employee_id})
    return jsonify({"message": "employee deleted"}), 200
