from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    from .cars import cars_bp
    from .customers import customers_bp
    from .employees import employees_bp

    app.register_blueprint(cars_bp, url_prefix="/api/cars")
    app.register_blueprint(customers_bp, url_prefix="/api/customers")
    app.register_blueprint(employees_bp, url_prefix="/api/employees")

    return app
