"""Main game-progression models."""

from app.extensions import db


class Section(db.Model):
    __tablename__ = 'section'

    section_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_steps = db.Column(db.Integer, nullable=False)
    unlock_xp = db.Column(db.Integer, nullable=False)

    # Relationships
    user_progress = db.relationship("UserProgress", back_populates="section")

    def to_dict(self):
        return {
            "sectionId": self.section_id,
            "totalSteps": self.total_steps,
            "unlockXP": self.unlock_xp
        }


class UserProgress(db.Model):
    __tablename__ = 'user_progress'

    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.section_id', ondelete='CASCADE'), primary_key=True)
    current_xp = db.Column(db.Integer, default=0)
    completed_status = db.Column(db.Boolean, default=False)

    # Relationships
    section = db.relationship("Section", back_populates="user_progress")
    user = db.relationship("User", back_populates="user_progress")

    def to_dict(self):
        return {
            "userId": self.user_id,
            "sectionId": self.section_id,
            "currentXp": self.current_xp,
            "completedStatus": self.completed_status
        }
