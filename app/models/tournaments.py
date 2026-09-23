"""Tournament player model."""

import uuid

from app.extensions import db


class TournamentPlayer(db.Model):
    __tablename__ = 'tournament_player'
    
    tournament_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    points = db.Column(db.Integer, default=0)
    matches_played = db.Column(db.Integer, default=0)
    final_rank = db.Column(db.Integer, default=0)
    prize_presented = db.Column(db.Boolean, default=False)
    seed = db.Column(db.Integer, default=1000)
    start_time = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'))
    last_sync_time = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'))

    user = db.relationship('User', backref='tournament_player')

    def to_dict(self):
        return {
            "tournamentId": self.tournament_id,
            "userId": self.user_id,
            "points": self.points,
            "matchesPlayed": self.matches_played,
            "finalRank": self.final_rank,
            "seed": self.seed,
            "prizePresented": self.prize_presented,
            "startTime": self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else None,
            "lastSyncTime": self.last_sync_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_sync_time else None
        }
