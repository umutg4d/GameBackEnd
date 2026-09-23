"""User badge endpoints."""

from flask import Blueprint, abort, jsonify, request

from app.api.validation import validate_json_request, validate_query_input
from app.extensions import db
from app.models import UserBadge
from app.schemas import UpdateUserBadgeRequest
from app.schemas.requests import SnakeCaseUserRequest


badges_blueprint = Blueprint("badges", __name__)


@badges_blueprint.get("/get-user-badges")
@validate_query_input(SnakeCaseUserRequest)
def get_user_badges():
    user_id = request.args.get("user_id")
    if not user_id:
        abort(400, description="User ID is required")

    badges = UserBadge.query.filter_by(user_id=user_id).all()

    return jsonify(dict({"status": "success", "badges": [badge.to_dict() for badge in badges]}))


@badges_blueprint.post("/update-user-badge")
def update_user_badge():
    command = validate_json_request(UpdateUserBadgeRequest)

    user_badge = UserBadge(
        user_id=command.user_id,
        badge_id=command.badge_id,
    )
    db.session.add(user_badge)
    db.session.commit()

    return jsonify(dict({"status": True, "message": "Updated user badge successfully", "userBadge": user_badge.to_dict()}))
