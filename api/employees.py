from flask import Blueprint, jsonify, request

employees_bp = Blueprint("employees", __name__)

employees = [
    {"id": 1, "name": "Jonas", "address": "adressenr", "branch": "harkjedunomed"},
    {"id": 2, "name": "Ponas", "address": "adressenr", "branch": "harkjeduhellenomed"}
]

@employees_bp.route("/", methods=["GET"])
def get_employees():
    return jsonify(employees)


@employees_bp.route("/", methods=["POST"])
def create_employees():
    data = request.get_json()
    
    if not all(field in data for field in ["name", "address", "branch"]):
        return jsonify({"message": "missing required fields"})

    new_employee = {
        "id": employees[-1]["id"] + 1 if employees else 1,
        "name": data["name"],
        "age": data["age"],
        "address": data["address"]
    }

    employees.append(new_employee)

    return jsonify(new_employee)


@employees_bp.route("/<int:employee_id>", methods=["PUT"])
def update_employees(employee_id):
    data = request.get_json()
    
    employee = next((employee for employee in employees if employee["id"] == employee_id), None)

    if employee is None:
        return jsonify({"message", "employee not found"})

    employee["name"] = data.get("name", employee["name"])
    employee["address"] = data.get("address", employee["address"])
    employee["branch"] = data.get("branch", employee["branch"])

    return jsonify(employees)


@employees_bp.route("/<int:employee_id>", methods=["DELETE"])
def delete_employees(employee_id):
    employee = next((employee for employee in employees if employee["id"] == employee_id), None)

    if employee == None:
        return jsonify({"message": "employee not found"})

    employees.remove(employee)

    return jsonify(employees)

