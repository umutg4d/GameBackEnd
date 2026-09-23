"""Daily user-statistics endpoints."""

import flask
from flask import Blueprint, jsonify

from app.api.validation import validate_query_input
from app.extensions import db
from app.models import UserDailyStatistics
from app.schemas.requests import UpdateDailyStatisticsRequest


statistics_blueprint = Blueprint("statistics", __name__)


@statistics_blueprint.post("/update-user-daily-stats")
@validate_query_input(UpdateDailyStatisticsRequest)
def update_user_daily_stats():

    if 'user_id' in flask.request.args:
        user_id = flask.request.args.get('user_id')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "User ID is required"}))
    
    if 'stat_date' in flask.request.args:
        stat_date = flask.request.args.get('stat_date')
    else:
        print("Stat date is required")
        return jsonify(dict({"status": False, "message": "Stat Date is required"}))

    if 'stat_name' in flask.request.args:
        stat_name = flask.request.args.get('stat_name')
    else:
        print("Stat name is required")
        return jsonify(dict({"status": False, "message": "Stat name is required"}))
    
    if 'delta_count' in flask.request.args:
        delta_count = flask.request.args.get('delta_count')
    else:
        print("Delta count is required")
        return jsonify(dict({"status": False, "message": "Delta count is required"}))

    user_statistics = UserDailyStatistics.query.filter_by(user_id=user_id, stat_date=stat_date).first()
    if user_statistics is None:
        user_statistics = UserDailyStatistics(user_id=user_id, stat_date=stat_date, session_count=0, puzzles_played=0, pieces_connected=0)
        if stat_name == 'session_count':
            user_statistics.session_count += int(delta_count)
        if stat_name == 'puzzle_count':
            user_statistics.puzzles_played += int(delta_count)
        if stat_name == 'pieces_connected':
            user_statistics.pieces_connected += int(delta_count)
        if stat_name == 'daily_gift':
            user_statistics.daily_gift += int(delta_count)
        if stat_name == 'tarot_offer':
            user_statistics.tarot_offer += int(delta_count)
        if stat_name == 'impossible_offer':
            user_statistics.impossible_offer += int(delta_count)
        if stat_name == 'daily_mission':
            user_statistics.daily_mission += int(delta_count)
        if stat_name == 'catventure':
            user_statistics.catventure += int(delta_count)
        if stat_name == 'spin_wheel':
            user_statistics.spin_wheel += int(delta_count)
        if stat_name == 'spin_count':
            user_statistics.spin_count += int(delta_count)
        if stat_name == 'multiplayer':
            user_statistics.multiplayer += int(delta_count)
        if stat_name == 'multiplayer_win':
            user_statistics.multiplayer_win += int(delta_count)
        if stat_name == 'daily_level_completed':
            user_statistics.daily_level_completed += int(delta_count)
        
        db.session.add(user_statistics)
        db.session.commit()
        return jsonify(dict({"status": True, "message": "Updated user daily statistics successfully", "userStatistics": user_statistics.to_dict()}))
    else:
        
        if stat_name == 'session_count':
            user_statistics.session_count += int(delta_count)
        if stat_name == 'puzzle_count':
            user_statistics.puzzles_played += int(delta_count)
        if stat_name == 'pieces_connected':
            user_statistics.pieces_connected += int(delta_count)
        if stat_name == 'daily_gift':
            user_statistics.daily_gift += int(delta_count)
        if stat_name == 'tarot_offer':
            user_statistics.tarot_offer += int(delta_count)
        if stat_name == 'impossible_offer':
            user_statistics.impossible_offer += int(delta_count)
        if stat_name == 'daily_mission':
            user_statistics.daily_mission += int(delta_count)
        if stat_name == 'catventure':
            user_statistics.catventure += int(delta_count)
        if stat_name == 'spin_wheel':
            user_statistics.spin_wheel += int(delta_count)
        if stat_name == 'multiplayer':
            user_statistics.multiplayer += int(delta_count)
        if stat_name == 'spin_count':
            user_statistics.spin_count += int(delta_count)
        if stat_name == 'multiplayer_win':
            user_statistics.multiplayer_win += int(delta_count)
        if stat_name == 'daily_level_completed':
            user_statistics.daily_level_completed += int(delta_count)

        db.session.add(user_statistics)
        db.session.commit()
        return jsonify(dict({"status": True, "message": "Updated user daily statistics successfully", "userStatistics": user_statistics.to_dict()}))
