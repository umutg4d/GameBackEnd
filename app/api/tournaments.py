"""Tournament-player endpoints."""

import flask
from flask import Blueprint, abort, jsonify

from app.api.validation import validate_json_input, validate_query_input
from app.extensions import db
from app.models import TournamentPlayer
from app.schemas.requests import CreateTournamentRequest, SnakeCaseUserRequest, UpdateTournamentRequest


tournaments_blueprint = Blueprint("tournaments", __name__)


@tournaments_blueprint.get("/get-tournament-info")
@validate_query_input(SnakeCaseUserRequest)
def get_tournament_info():

    if 'user_id' in flask.request.args:
        user_id = flask.request.args.get('user_id')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "Tournament ID is required"}))
    
    tournament_player = TournamentPlayer.query.filter_by(user_id=user_id, prize_presented =False).first()
    
    if tournament_player is None:
        abort(404, description="Tournament player not found")
    
    return jsonify(dict({"status": "success", "tournamentInfo": tournament_player.to_dict() if tournament_player else None}))


@tournaments_blueprint.post("/create-tournament-info")
@validate_query_input(CreateTournamentRequest)
def create_tournament_info():

    if 'user_id' in flask.request.args:
        user_id = flask.request.args.get('user_id')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "User ID is required"}))
    
    if 'seed' in flask.request.args:
        seed = flask.request.args.get('seed')
    else:
        print("Seed is required")
        return jsonify(dict({"status": False, "message": "Seed is required"}))

    tournament_player = TournamentPlayer(user_id=user_id, seed=seed)

    
    db.session.add(tournament_player)
    db.session.commit()

    return jsonify(dict({"status": True, "message": "Created tournament player successfully", "tournamentInfo": tournament_player.to_dict()}))


@tournaments_blueprint.post("/update-tournament-info")
@validate_json_input(UpdateTournamentRequest)
def update_tournament_info():
    data = flask.request.get_json()

    # Required identifiers
    tournament_id = data.get("tournamentId")
    user_id = data.get("userId")

    if not tournament_id or not user_id:
        return jsonify({"error": "tournamentId and userId are required"}), 400

    # Find the tournament player record
    player = TournamentPlayer.query.filter_by(
        tournament_id=tournament_id,
        user_id=user_id
    ).first()

    if not player:
        abort(404, description="Tournament player not found")

    # Update only if values are provided in request
    if "points" in data:
        player.points = data["points"]

    if "matchesPlayed" in data:
        player.matches_played = data["matchesPlayed"]

    if "finalRank" in data:
        player.final_rank = data["finalRank"]

    if "prizePresented" in data:
        player.prize_presented = data["prizePresented"]

    db.session.commit()
    return jsonify(dict({"status": True, "message": "Updated successfully", "tournamentInfo": player.to_dict()}))
