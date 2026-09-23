"""Daily-level completion and reward models."""

from app.extensions import db


class DailyLevelCompletion(db.Model):
    __tablename__ = 'daily_level_completions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'))
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    completed_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'))

    # Relationship back to user
    user = db.relationship('User', backref=db.backref('daily_level_completions', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            "day": self.day,
            "month": self.month,
            "year": self.year,
            "completed_at": self.completed_at.strftime('%Y-%m-%d %H:%M:%S') if self.completed_at else None
        }


class DailyLevelRewardClaimed(db.Model):
    __tablename__ = 'daily_level_rewards_claimed'

    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    milestone = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    claimed_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'))

    # Relationship back to user
    user = db.relationship('User', backref=db.backref('daily_level_rewards_claimed', cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            "milestone": self.milestone,
            "month": self.month,
            "year": self.year,
            "claimed_at": self.claimed_at.strftime('%Y-%m-%d %H:%M:%S') if self.claimed_at else None
        }
