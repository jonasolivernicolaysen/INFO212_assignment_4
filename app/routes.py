from flask import Blueprint

# Create a blueprint for the main routes
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Hello, Flask!"
