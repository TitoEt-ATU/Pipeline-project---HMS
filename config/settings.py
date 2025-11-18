import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", 
        "sqlite:///mydatabase.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    
    # Application settings
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Ensure we're using PostgreSQL in production
    if "postgresql" not in Config.SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = "postgresql://localhost/hospital_management"


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


# Select configuration based on environment
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}

current_config = config_by_name.get(
    os.environ.get("FLASK_ENV", "development"), 
    DevelopmentConfig
)
