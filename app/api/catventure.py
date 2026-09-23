"""Catventure progression endpoints."""

import flask
from flask import Blueprint, jsonify

from app.api.validation import validate_query_input
from app.extensions import db
from app.models import CatventureLevelProgress
from app.schemas.requests import SnakeCaseUserRequest, UpdateCatventureProgressRequest


catventure_blueprint = Blueprint("catventure", __name__)


@catventure_blueprint.get("/get-catventure-new-progress")
@validate_query_input(SnakeCaseUserRequest)
def get_catventure_progress():
    if 'user_id' in flask.request.args:
        user_id = flask.request.args.get('user_id')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "User ID is required"}))
    
    catventure_progress = CatventureLevelProgress.query.filter_by(user_id=user_id).first()
    if catventure_progress is None:
        catventure_level_progress = CatventureLevelProgress(user_id=user_id, current_section_id=1, current_level_id=1)
        db.session.add(catventure_level_progress)
        db.session.commit()
        return jsonify(dict({"status": True, "message": "Success", "catventureProgress": catventure_level_progress.to_dict()}))
    
    return jsonify(dict({"status": True, "message": "Success", "catventureProgress": catventure_progress.to_dict()}))


@catventure_blueprint.post("/update-catventure-progress")
@validate_query_input(UpdateCatventureProgressRequest)
def update_catventure_progress():
    if 'user_id' in flask.request.args:
        user_id = flask.request.args.get('user_id')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "User ID is required"}))
    
    if 'current_section_id' in flask.request.args:
        current_section_id = flask.request.args.get('current_section_id')
    else:
        print("Current Section ID is required")
        return jsonify(dict({"status": False, "message": "Current Section ID is required"}))
    
    if 'current_level_id' in flask.request.args:
        current_level_id = flask.request.args.get('current_level_id')
    else:
        print("Current Level ID is required")
        return jsonify(dict({"status": False, "message": "Current Level ID is required"}))
    
    catventure_progress = CatventureLevelProgress.query.filter_by(user_id=user_id).first()
    if catventure_progress is None:
        catventure_progress = CatventureLevelProgress(user_id=user_id, current_section_id=current_section_id, current_level_id=current_level_id)
        db.session.add(catventure_progress)
        db.session.commit()
        return jsonify(dict({"status": True, "message": "Updated catventure progress successfully", "catventureProgress": catventure_progress.to_dict()}))
    else:
        catventure_progress.current_section_id = current_section_id
        catventure_progress.current_level_id = current_level_id
        db.session.commit()
        return jsonify(dict({"status": True, "message": "Updated catventure progress successfully", "catventureProgress": catventure_progress.to_dict()}))
