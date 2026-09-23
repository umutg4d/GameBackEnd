"""Badge models."""

from app.extensions import db


class Badge(db.Model):
    __tablename__ = 'badges'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    icon_path = db.Column(db.String(255))


class UserBadge(db.Model):
    __tablename__ = 'user_badges'

    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id'), primary_key=True)
    earned_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'))

    def to_dict(self):
        return {
            "userId": self.user_id,
            "badgeId": self.badge_id,
            "earnedAt": self.earned_at.strftime('%Y-%m-%d %H:%M:%S') if self.earned_at else None
        }
