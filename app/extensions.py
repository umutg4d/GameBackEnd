"""Shared Flask extension instances.

Extensions are created without binding them to a Flask application. The
application factory initializes them later, which keeps application creation
testable and prevents route and model modules from importing a global app.
"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
