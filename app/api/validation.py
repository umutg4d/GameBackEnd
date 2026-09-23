"""Reusable validation helpers for HTTP request inputs."""

from functools import wraps
from typing import Any, TypeVar

from flask import abort, request
from pydantic import BaseModel, ValidationError


SchemaType = TypeVar("SchemaType", bound=BaseModel)


def require_json_object() -> dict[str, Any]:
    """Return a JSON object or raise a descriptive HTTP error."""

    if not request.is_json:
        abort(415, description="Request content type must be application/json")

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, description="Request body must be a valid JSON object")

    return data


def validate_json_request(schema: type[SchemaType]) -> SchemaType:
    """Parse the request body with a Pydantic schema."""

    return _validate(schema, require_json_object())


def validate_query_request(schema: type[SchemaType]) -> SchemaType:
    """Parse query parameters with a Pydantic schema."""

    return _validate(schema, request.args.to_dict(flat=True))


def validate_json_input(schema: type[SchemaType]):
    """Validate JSON before invoking a route function."""

    def decorator(view):
        @wraps(view)
        def validated_view(*args, **kwargs):
            validate_json_request(schema)
            return view(*args, **kwargs)

        return validated_view

    return decorator


def validate_query_input(schema: type[SchemaType]):
    """Validate query parameters before invoking a route function."""

    def decorator(view):
        @wraps(view)
        def validated_view(*args, **kwargs):
            validate_query_request(schema)
            return view(*args, **kwargs)

        return validated_view

    return decorator


def _validate(
    schema: type[SchemaType],
    data: dict[str, Any],
) -> SchemaType:
    """Validate data and translate failures into safe HTTP errors."""

    try:
        return schema.model_validate(data)
    except ValidationError as error:
        messages = []
        for issue in error.errors(include_input=False, include_url=False):
            location = ".".join(str(part) for part in issue["loc"])
            messages.append(f"{location}: {issue['msg']}")

        description = "; ".join(messages) or "Invalid request body"
        abort(400, description=f"Request validation failed: {description}")
