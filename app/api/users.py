"""User account endpoints."""

import flask
from flask import Blueprint, abort, jsonify

from app.api.validation import validate_query_input
from app.extensions import db
from app.models import User, UserDailyStatistics
from app.schemas.requests import CreateUserRequest, GetUserRequest, UpdateUserRequest


users_blueprint = Blueprint("users", __name__)


@users_blueprint.get("/get-user")
@validate_query_input(GetUserRequest)
def get_user():
    if 'idfv' in flask.request.args:
        idfv = flask.request.args.get('idfv')
    else:
        print("IDFV is required")
        return jsonify(dict({"status": "error", "message": "IDFV is required"}))

    if 'stat_date' in flask.request.args:
        stat_date = flask.request.args.get('stat_date')
    else:
        print("Stat date is required")
        return jsonify(dict({"status": False, "message": "Stat Date is required"}))
    
    #get users with idfv equals this parameter
    user = User.query.filter_by(idfv=idfv).first()

    if user is None:
        abort(404, description="User not found")
    
    user_statistics = UserDailyStatistics.query.filter_by(user_id=user.user_id, stat_date=stat_date).first()
    if user_statistics is None:
        user_statistics = UserDailyStatistics(user_id=user.user_id, stat_date=stat_date, session_count=1, puzzles_played=0, pieces_connected=0, daily_gift=0, tarot_offer=0, impossible_offer=0, daily_mission=0, catventure=0, multiplayer=0)
        db.session.add(user_statistics)
        db.session.commit()
    else:
        user_statistics.session_count += 1
        db.session.commit()
    
    return jsonify(dict({"status": "success", "user": user.to_dict(), "user_statistics": user_statistics.to_dict()}))


@users_blueprint.post("/create-user")
@validate_query_input(CreateUserRequest)
def create_user():

    if 'idfv' in flask.request.args:
        idfv = flask.request.args.get('idfv')
    else:
        print("IDFV is required")
        return jsonify(dict({"status": "error", "message": "IDFV is required"}))
    
    if 'stat_date' in flask.request.args:
        stat_date = flask.request.args.get('stat_date')
    else:
        print("Stat date is required")
        return jsonify(dict({"status": False, "message": "Stat Date is required"}))
    
    user = User(idfv=idfv)
    db.session.add(user)
    db.session.commit()

    user_statistics = UserDailyStatistics(user_id=user.user_id, stat_date=stat_date, session_count=1, puzzles_played=0, pieces_connected=0)
    db.session.add(user_statistics)
    db.session.commit()

    return jsonify(dict({"status": "success", "message": "Inserted successfully", "user": user.to_dict(), "user_statistics": user_statistics.to_dict()}))


@users_blueprint.post("/update-user")
@validate_query_input(UpdateUserRequest)
def update_user():
    print("Updating user")
    if 'user_id' in flask.request.args:
        user_id = flask.request.args.get('user_id')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "User ID is required"}))

    if 'vip_status' in flask.request.args:
        vip_status = flask.request.args.get('vip_status')
    else:
        print("VIP Status is required")
        return jsonify(dict({"status": False, "message": "VIP Status is required"}))
    
    if 'no_ads_status' in flask.request.args:
        no_ads_status = flask.request.args.get('no_ads_status')
    else:
        print("No Ads Status is required")
        return jsonify(dict({"status": False, "message": "No Ads Status is required"}))

    if 'soft_currency' in flask.request.args:
        soft_currency = flask.request.args.get('soft_currency')
    else:
        print("Soft Currency is required")
        return jsonify(dict({"status": False, "message": "Soft Currency is required"}))

    if 'hint_count' in flask.request.args:
        hint_count = flask.request.args.get('hint_count')
    else:
        print("Hint count is required")
        return jsonify(dict({"status": False, "message": "Hint count is required"}))

    if 'match_count' in flask.request.args:
        match_count = flask.request.args.get('match_count')
    else:
        print("Match count is required")
        return jsonify(dict({"status": False, "message": "Hint count is required"}))

    
    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
        abort(404, description="User not found")

    user.vip_status = vip_status == 'True'
    user.no_ads_status = no_ads_status == 'True'
    user.soft_currency = soft_currency
    user.hint_count = hint_count
    user.match_count = match_count
    db.session.commit()

    return jsonify(dict({"status": True, "message": "Updated successfully", "user": user.to_dict()}))
