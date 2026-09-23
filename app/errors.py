"""Central JSON error handling for the Flask application."""

from flask import Flask, current_app, jsonify
from werkzeug.exceptions import HTTPException

from app.extensions import db


def register_error_handlers(app: Flask) -> None:
    """Register application-wide handlers for unhandled errors."""

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        response = jsonify(
            {
                "status": "error",
                "message": error.description,
            }
        )
        response.status_code = error.code or 500

        original_response = error.get_response()
        for header in ("Allow", "Retry-After", "WWW-Authenticate"):
            if header in original_response.headers:
                response.headers[header] = original_response.headers[header]

        return response

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        try:
            db.session.rollback()
        except Exception:
            current_app.logger.exception(
                "Failed to roll back the database session after an error"
            )

        current_app.logger.exception("Unhandled application error", exc_info=error)

        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Internal server error",
                }
            ),
            500,
        )
