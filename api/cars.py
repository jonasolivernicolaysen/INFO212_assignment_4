from flask import Blueprint, jsonify, request
from .db import db

cars_bp = Blueprint("cars", __name__)

@cars_bp.route("/", methods=["GET"])
def get_cars():
    query = "MATCH (c:Car) RETURN c"
    result = db.query(query)
    cars = [record["c"]._properties for record in result]
    return jsonify(cars), 200


@cars_bp.route("/", methods=["POST"])
def create_cars():
    data = request.get_json()
    
    if not all(field in data for field in ["make", "model", "year", "location"]):
        return jsonify({"message": "missing required fields"})

    query = """
    CREATE (c:Car {id: $id, make: $make, model: $model, year: $year, location: $location, status: $status})
    RETURN c
    """

    car_id = len(db.query("MATCH (c:Car) RETURN c")) + 1

    parameters = {
        "id": car_id,
        "make": data["make"],
        "model": data["model"],
        "year": data["year"],
        "location": data["location"],
        "status": data.get("status", "available")
    }

    result = db.query(query, parameters)
    new_car = result[0]["c"]._properties
    return jsonify(new_car), 201



@cars_bp.route("/<int:car_id>", methods=["PUT"])
def update_cars(car_id):
    data = request.get_json()
    
    car_query = "MATCH (c:Car {id: $id}) RETURN c"
    car_result = db.query(car_query, {"id": car_id})
    if not car_result:
        return jsonify({"message": "car not found"})

    update_query = """
    MATCH (c:Car {id: $id})
    SET c.make = $make, c.model = $model, c.year = $year, c.location = $location, c.status = $status
    RETURN c
    """

    parameters = {
        "id": car_id,
        "make": data.get("make", car_result[0]["c"]["make"]),
        "model": data.get("model", car_result[0]["c"]["model"]),
        "year": data.get("year", car_result[0]["c"]["year"]),
        "location": data.get("location", car_result[0]["c"]["location"]),
        "status": data.get("status", car_result[0]["c"]["status"])
    }

    result = db.query(update_query, parameters)
    updated_car = result[0]["c"]._properties
    return jsonify(updated_car), 200


@cars_bp.route("/<int:car_id>", methods=["DELETE"])
def delete_cars(car_id):    
    car_query = "MATCH (c:Car {id: $id}) RETURN c"
    car_result = db.query(car_query, {"id": car_id})
    if not car_result:
        return jsonify({"message": "car not found"}), 404
    
    delete_query = "MATCH (c:Car {id: $id}) DELETE c"
    db.query(delete_query, {"id": car_id})
    return jsonify({"message": "car deleted"}), 200
    

