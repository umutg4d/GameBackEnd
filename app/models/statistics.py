"""Daily user-statistics model."""

from app.extensions import db


class UserDailyStatistics(db.Model):
    __tablename__ = 'user_daily_statistics'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    stat_date = db.Column(db.DATE, nullable=False)
    session_count = db.Column(db.Integer, default=0)
    puzzles_played = db.Column(db.Integer, default=0)
    pieces_connected = db.Column(db.Integer, default=0)
    daily_gift = db.Column(db.Integer, default=0)
    tarot_offer = db.Column(db.Integer, default=0)
    impossible_offer = db.Column(db.Integer, default=0)
    daily_mission = db.Column(db.Integer, default=0)
    catventure = db.Column(db.Integer, default=0)
    spin_wheel = db.Column(db.Integer, default=0)
    multiplayer = db.Column(db.Integer, default=0)
    spin_count = db.Column(db.Integer, default=0)
    multiplayer_win = db.Column(db.Integer, default=0)
    daily_level_completed = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'))

    user = db.relationship('User', back_populates='user_daily_statistics')

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "statDate": self.stat_date,
            "sessionCount": self.session_count,
            "puzzlesPlayed": self.puzzles_played,
            "piecesConnected": self.pieces_connected,
            "dailyGift": self.daily_gift,
            "tarotOffer": self.tarot_offer,
            "impossibleOffer": self.impossible_offer,
            "dailyMission": self.daily_mission,
            "catventure": self.catventure,
            "spinWheel": self.spin_wheel,
            "multiplayer": self.multiplayer,
            "spinCount": self.spin_count,
            "multiplayerWin": self.multiplayer_win,
            "dailyLevelCompleted": self.daily_level_completed,
            "lastUpdatedAt": self.last_updated.strftime('%Y-%m-%d %H:%M:%S') if self.last_updated else None
        }
