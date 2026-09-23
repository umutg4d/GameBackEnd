"""Database connection and SQLAlchemy engine configuration."""

import atexit
from threading import Lock
from typing import Any, Callable, Mapping

import pymysql
from flask import Flask
from google.cloud.sql.connector import Connector, IPTypes


ConnectionCreator = Callable[[], pymysql.connections.Connection]


def build_connection_creator(config: Mapping[str, Any]) -> ConnectionCreator:
    """Build the connection callback consumed by SQLAlchemy's connection pool.

    Development connects directly to the configured MySQL host. Other runtime
    environments connect through the Cloud SQL Python Connector. Configuration
    is captured once when the application starts rather than read for every
    new database connection.
    """

    environment = str(config.get("ENVIRONMENT", "DEVELOPMENT")).upper()
    host = config.get("DB_HOST")
    user = config.get("DB_USER")
    password = config.get("DB_PASSWORD")
    database = config.get("DB_NAME")
    ip_type = IPTypes.PRIVATE if config.get("PRIVATE_IP") else IPTypes.PUBLIC

    connector: Connector | None = None
    connector_lock = Lock()

    def get_connector() -> Connector:
        nonlocal connector

        if connector is None:
            with connector_lock:
                if connector is None:
                    connector = Connector(ip_type=ip_type)
                    atexit.register(connector.close)

        return connector

    def connect() -> pymysql.connections.Connection:
        if environment == "DEVELOPMENT":
            return pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
            )

        return get_connector().connect(
            host,
            "pymysql",
            user=user,
            password=password,
            db=database,
        )

    return connect


def configure_database(app: Flask) -> None:
    """Apply database engine configuration to a Flask application."""

    if app.config.get("TESTING"):
        return

    engine_options = dict(app.config.get("SQLALCHEMY_ENGINE_OPTIONS", {}))
    engine_options.update(
        {
            "creator": build_connection_creator(app.config),
            "pool_size": 50,
            "max_overflow": 50,
            "pool_timeout": 30,
            "pool_recycle": 1800,
            "pool_pre_ping": True,
        }
    )
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = engine_options
