"""Daily-level completion and reward endpoints."""

from datetime import datetime

import flask
from flask import Blueprint, jsonify

from app.api.validation import validate_query_input
from app.extensions import db
from app.models import DailyLevelCompletion, DailyLevelRewardClaimed
from app.schemas.requests import ClaimDailyLevelRewardRequest, CompleteDailyLevelRequest, SnakeCaseUserRequest


daily_levels_blueprint = Blueprint("daily_levels", __name__)


@daily_levels_blueprint.get("/get-daily-levels-info")
@validate_query_input(SnakeCaseUserRequest)
def get_user_daily_levels():
    if 'user_id' in flask.request.args:
        user_id = flask.request.args.get('user_id')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "User ID is required"}))
    
    now = datetime.now()
    current_month = now.month
    current_year = now.year

    completed_daily_levels = DailyLevelCompletion.query.filter_by(user_id=user_id, month=current_month, year=current_year).all()
    daily_level_rewards_claimed = DailyLevelRewardClaimed.query.filter_by(user_id=user_id, month=current_month, year=current_year).all()

    return jsonify(dict({"status": True, "message": "Success", "completed_daily_levels": [daily_level.to_dict() for daily_level in completed_daily_levels], "rewards_claimed": [daily_level_reward.to_dict() for daily_level_reward in daily_level_rewards_claimed]}))


@daily_levels_blueprint.post("/complete-daily-level")
@validate_query_input(CompleteDailyLevelRequest)
def complete_daily_level():
    if 'user_id' in flask.request.args:
        user_id = flask.request.args.get('user_id')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "User ID is required"}))
    
    if 'day' in flask.request.args:
        day = flask.request.args.get('day')
    else:
        print("Day is required")
        return jsonify(dict({"status": False, "message": "Day is required"}))
    
    if 'month' in flask.request.args:
        month = flask.request.args.get('month')
    else:
        print("Month is required")
        return jsonify(dict({"status": False, "message": "Month is required"}))
    
    if 'year' in flask.request.args:
        year = flask.request.args.get('year')
    else:
        print("Year is required")
        return jsonify(dict({"status": False, "message": "Year is required"}))
    
    daily_level = DailyLevelCompletion(user_id=user_id, day=day, month=month, year=year)
    db.session.add(daily_level)
    db.session.commit()

    return jsonify(dict({"status": True, "message": "Completed daily level successfully", "daily_level": daily_level.to_dict()}))


@daily_levels_blueprint.post("/claim-daily-level-reward")
@validate_query_input(ClaimDailyLevelRewardRequest)
def claim_daily_level_reward():

    if 'user_id' in flask.request.args:
        user_id = flask.request.args.get('user_id')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "User ID is required"}))
    
    if 'milestone' in flask.request.args:
        milestone = flask.request.args.get('milestone')
    else:
        print("Milestone is required")
        return jsonify(dict({"status": False, "message": "Milestone is required"}))
    
    if 'month' in flask.request.args:
        month = flask.request.args.get('month')
    else:
        print("Month is required")
        return jsonify(dict({"status": False, "message": "Month is required"}))
    
    if 'year' in flask.request.args:
        year = flask.request.args.get('year')
    else:
        print("Year is required")
        return jsonify(dict({"status": False, "message": "Year is required"}))
    
    daily_level_reward = DailyLevelRewardClaimed(user_id=user_id, milestone=milestone, month=month, year=year)
    db.session.add(daily_level_reward)
    db.session.commit()

    return jsonify(dict({"status": True, "message": "Claimed daily level reward successfully", "daily_level_reward": daily_level_reward.to_dict()}))
