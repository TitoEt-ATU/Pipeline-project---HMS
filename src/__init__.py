from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.settings import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from .routes.patients import patients_bp
    from .routes.doctors import doctors_bp
    from .routes.appointments import appointments_bp
    from .routes.dashboard import dashboard_bp

    app.register_blueprint(patients_bp, url_prefix='/patients')
    app.register_blueprint(doctors_bp, url_prefix='/doctors')
    app.register_blueprint(appointments_bp, url_prefix='/appointments')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    return app
