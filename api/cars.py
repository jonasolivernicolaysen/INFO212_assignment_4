from flask import Blueprint, jsonify, request

cars_bp = Blueprint("cars", __name__)

cars = []

@cars_bp.route("/", methods=["GET"])
def get_cars():
    pass

@cars_bp.route("/", methods=["POST"])
def get_cars():
    pass

@cars_bp.route("/", methods=["PUT"])
def get_cars():
    pass

@cars_bp.route("/", methods=["DELETE"])
def get_cars():
    pass
