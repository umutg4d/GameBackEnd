"""User mission model."""

from app.extensions import db


class UserMission(db.Model):
    __tablename__ = 'user_missions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    mission_id = db.Column(db.Integer, nullable=False)
    step = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'))

    user = db.relationship('User', back_populates='user_missions')

    def to_dict(self):
        return {
            "userId": self.user_id,
            "missionId": self.mission_id,
            "step": self.step,
            "completedAt": self.completed_at.strftime('%Y-%m-%d %H:%M:%S') if self.completed_at else None
        }
