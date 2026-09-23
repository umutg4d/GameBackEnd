"""Main game-progression endpoints."""

import flask
from flask import Blueprint, jsonify
from sqlalchemy import and_

from app.api.validation import validate_query_input
from app.extensions import db
from app.models import UserProgress
from app.schemas.requests import SnakeCaseUserRequest, UpdateUserProgressRequest


progression_blueprint = Blueprint("progression", __name__)


@progression_blueprint.get("/get-current-user-progress")
@validate_query_input(SnakeCaseUserRequest)
def get_user_progress():
    if 'user_id' in flask.request.args:
        user_id = flask.request.args.get('user_id')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "User ID is required"}))
    
    progress_objects = UserProgress.query.filter(and_(UserProgress.user_id==user_id, UserProgress.completed_status ==False)).all()    

    if len(progress_objects) == 0:
        progress_objects = []
        progress = UserProgress(user_id=user_id, section_id=1, completed_status=False)
        db.session.add(progress)
        db.session.commit()
        progress_objects.append(progress)
    
    return jsonify(dict({"status": True, "message": "Success", "userProgress": [progress.to_dict() for progress in progress_objects]}))


@progression_blueprint.post("/update-user-progress")
@validate_query_input(UpdateUserProgressRequest)
def update_user_progress():
    if 'user_id' in flask.request.args:
        user_id = flask.request.args.get('user_id')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "User ID is required"}))
    
    if 'section_id' in flask.request.args:
        section_id = flask.request.args.get('section_id')
    else:
        print("Section ID is required")
        return jsonify(dict({"status": False, "message": "Section ID is required"}))
    
    if 'current_xp' in flask.request.args:
        current_xp = flask.request.args.get('current_xp')
    else:
        print("Current XP is required")
        return jsonify(dict({"status": False, "message": "Current XP is required"}))
    
    if 'completed_status' in flask.request.args:
        completed_status = flask.request.args.get('completed_status')
    else:
        print("Completed Status is required")
        return jsonify(dict({"status": False, "message": "Completed Status is required"}))
    
    completed = True if completed_status == 'True' else False
    user_progress = UserProgress.query.filter_by(user_id=user_id, section_id=section_id).first()
    if user_progress is None:
        user_progress = UserProgress(user_id=user_id, section_id=section_id, current_xp=current_xp, completed_status=completed)
        db.session.add(user_progress)
        db.session.commit()
        return jsonify(dict({"status": True, "message": "Updated user progress successfully", "userProgress": user_progress.to_dict()}))
    else:
        user_progress.current_xp = current_xp
        user_progress.completed_status = completed
        db.session.commit()
        return jsonify(dict({"status": True, "message": "Updated user progress successfully", "userProgress": user_progress.to_dict()}))
