from flask import Flask
from config import Config
from .db import init_app

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_app(app)

    from .cars import cars_bp
    from .customers import customers_bp
    from .employees import employees_bp

    app.register_blueprint(cars_bp, url_prefix="/api/cars")
    app.register_blueprint(customers_bp, url_prefix="/api/customers")
    app.register_blueprint(employees_bp, url_prefix="/api/employees")

    return app
