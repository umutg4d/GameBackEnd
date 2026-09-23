"""Catventure section, level, and progress models."""

from app.extensions import db


class CatventureSection(db.Model):
    __tablename__ = 'sections'

    section_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    section_name = db.Column(db.String(50), nullable=False)

    # Relationships
    #user_catventure_progress = db.relationship("CatventureLevelProgress", back_populates="section")

    def to_dict(self):
        return {
            "sectionId": self.section_id,
            "sectionName": self.section_name
        }


class CatventureLevel(db.Model):
    __tablename__ = 'levels'

    level_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.section_id'), nullable=False)
    level_index = db.Column(db.Integer, nullable=False)
    level_name = db.Column(db.String(100), nullable=False)

    # Relationships
    #user_catventure_progress = db.relationship("CatventureLevelProgress", back_populates="level")

    def to_dict(self):
        return {
            "levelId": self.level_id,
            "sectionId": self.section_id,
            "levelIndex": self.level_index,
            "levelName": self.level_name
        }


class CatventureLevelProgress(db.Model):
    __tablename__ = 'user_catventure_progress'

    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), primary_key=True)
    current_section_id = db.Column(db.Integer, db.ForeignKey('sections.section_id'))
    current_level_id = db.Column(db.Integer, db.ForeignKey('levels.level_id'))
    updated_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'))

    # Relationships
    #level = db.relationship("CatventureLevel", back_populates="user_catventure_progress")
    #user = db.relationship("User", back_populates="user_catventure_progress")
    #section = db.relationship("CatventureSection", back_populates="user_catventure_progress")

    def to_dict(self):
        return {
            "userId": self.user_id,
            "current_section_id": self.current_section_id,
            "current_level_id": self.current_level_id,
            "updated_at": self.updated_at
        }
