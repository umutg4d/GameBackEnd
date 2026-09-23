"""Environment-based configuration for the Flask application."""

import os
from typing import Type


class BaseConfig:
    """Settings shared by every application environment."""

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # A database URI is required by Flask-SQLAlchemy during initialization.
    # app.database supplies the actual connection creator to the engine.
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "mysql+pymysql://",
    )

    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("GCSQL_USER_NAME")
    DB_PASSWORD = os.getenv("GCSQL_PASSWORD")
    DB_NAME = os.getenv("GCSQL_DB_NAME")
    PRIVATE_IP = os.getenv("PRIVATE_IP")


class DevelopmentConfig(BaseConfig):
    """Configuration used for local development."""

    DEBUG = True
    ENVIRONMENT = "DEVELOPMENT"


class TestingConfig(BaseConfig):
    """Configuration used by automated tests."""

    TESTING = True
    ENVIRONMENT = "TESTING"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URI",
        "sqlite:///:memory:",
    )


class ProductionConfig(BaseConfig):
    """Configuration used by deployed application instances."""

    ENVIRONMENT = "PRODUCTION"


CONFIGURATIONS: dict[str, Type[BaseConfig]] = {
    "DEVELOPMENT": DevelopmentConfig,
    "TESTING": TestingConfig,
    "PRODUCTION": ProductionConfig,
}


def get_config() -> Type[BaseConfig]:
    """Return the configuration class selected by ``ENVIRONMENT``."""

    environment = os.getenv("ENVIRONMENT", "DEVELOPMENT").strip().upper()

    try:
        return CONFIGURATIONS[environment]
    except KeyError as error:
        supported = ", ".join(CONFIGURATIONS)
        raise RuntimeError(
            f"Unsupported ENVIRONMENT {environment!r}. Expected one of: {supported}."
        ) from error


def validate_database_config(config: dict) -> None:
    """Raise a clear startup error when database settings are incomplete."""

    required_settings = ("DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME")
    missing_settings = [
        setting for setting in required_settings if not config.get(setting)
    ]

    if missing_settings:
        missing = ", ".join(missing_settings)
        raise RuntimeError(f"Missing required database configuration: {missing}")
