"""Daily mission endpoints."""

import flask
from flask import Blueprint, jsonify

from app.api.validation import validate_query_input
from app.extensions import db
from app.models import UserMission
from app.schemas.requests import ClaimMissionRequest, GetClaimedMissionsRequest


missions_blueprint = Blueprint("missions", __name__)


@missions_blueprint.get("/get-user-claimed-missions")
@validate_query_input(GetClaimedMissionsRequest)
def get_user_claimed_missions():

    if 'user_id' in flask.request.args:
        user_id = flask.request.args.get('user_id')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "User ID is required"}))

    if 'current_date' in flask.request.args:
        current_date = flask.request.args.get('current_date')
    else:
        print("Current Date is required")
        return jsonify(dict({"status": False, "message": "Current Date is required"}))
    
    user_missions = UserMission.query.filter_by(user_id=user_id, completed_at=current_date).all()

    if user_missions is None:
        print("No missions found")
        return jsonify(dict({"status": False, "message": "No Missions", "missions": []}))
    else:
        print([mission.to_dict() for mission in user_missions])
        return jsonify(dict({"status": True, "message": "Success", "missions": [mission.to_dict() for mission in user_missions]}))


@missions_blueprint.post("/claim-mission")
@validate_query_input(ClaimMissionRequest)
def user_claimed_mission():
    if 'user_id' in flask.request.args:
        user_id = flask.request.args.get('user_id')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "User ID is required"}))

    if 'current_date' in flask.request.args:
        current_date = flask.request.args.get('current_date')
    else:
        print("Current Date is required")
        return jsonify(dict({"status": False, "message": "Current Date is required"}))

    if 'mission_id' in flask.request.args:
        mission_id = flask.request.args.get('mission_id')
    else:
        print("Mission id is required")
        return jsonify(dict({"status": False, "message": "Mission id is required"}))
    
    if 'step' in flask.request.args:
        step = flask.request.args.get('step')
    else:
        print("Step is required")
        return jsonify(dict({"status": False, "message": "Step is required"}))
    
    user_mission = UserMission(user_id=user_id, mission_id=mission_id, step=step, completed_at=current_date)
    db.session.add(user_mission)
    db.session.commit()

    return jsonify(dict({"status": True, "message": "Updated user mission successfully", "user_mission": user_mission.to_dict()}))
