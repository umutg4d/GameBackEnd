"""Health and connectivity endpoints."""

from flask import Blueprint, jsonify


health_blueprint = Blueprint("health", __name__)


@health_blueprint.get("/get-test-response")
def get_test_response():
    return jsonify(dict({"status": True, "message": "Inserted successfully"}))
