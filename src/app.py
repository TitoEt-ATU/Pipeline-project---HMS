from flask import Flask
from config.settings import Config
from src.extensions import db, migrate
from flask_sqlalchemy import SQLAlchemy
from src.models import *

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def home():
        return "Hospital Management System API"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)