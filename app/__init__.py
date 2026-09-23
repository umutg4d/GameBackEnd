from importlib import import_module

from flask import Flask

from app.config import get_config
from app.database import configure_database
from app.errors import register_error_handlers
from app.extensions import db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config())

    configure_database(app)
    db.init_app(app)
    import_module("app.models")

    register_blueprints(app)
    register_error_handlers(app)

    return app


def register_blueprints(app: Flask) -> None:
    from app.api import BLUEPRINTS

    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)
