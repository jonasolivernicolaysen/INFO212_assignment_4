from flask import Blueprint, jsonify, request

cars_bp = Blueprint("cars", __name__)

cars = [
    {"id": 1, "make": "Toyota", "model": "Corolla", "year": 2020, "status": "available"},
    {"id": 2, "make": "Honda", "model": "Civic", "year": 2019, "status": "available"}
]

@cars_bp.route("/", methods=["GET"])
def get_cars():
    return jsonify(cars)


@cars_bp.route("/", methods=["POST"])
def create_cars():
    data = request.get_json()
    
    if not all(field in data for field in ["make", "model", "year", "location"]):
        return jsonify({"message": "missing required fields"})

    new_car = {
        "id": cars[-1]["id"] + 1 if cars else 1,
        "make": data["make"],
        "model": data["model"],
        "year": data["year"],
        "location": data["location"],
        "status": data.get("status", "available")
    }

    cars.append(new_car)

    return jsonify(new_car)


@cars_bp.route("/<int:car_id>", methods=["PUT"])
def update_cars(car_id):
    data = request.get_json()
    
    car = next((car for car in cars if car["id"] == car_id), None)

    if car is None:
        return jsonify({"message", "car not found"})

    car["make"] = data.get("make", car["make"])
    car["model"] = data.get("model", car["model"])
    car["year"] = data.get("year", car["year"])
    car["location"] = data.get("location", car["location"])
    car["status"] = data.get("status", car["status"])

    return jsonify(cars)


@cars_bp.route("/<int:car_id>", methods=["DELETE"])
def delete_cars(car_id):
    car = next((car for car in cars if car["id"] == car_id), None)

    if car == None:
        return jsonify({"message": "car not found"})

    cars.remove(car)

    return jsonify(cars)

