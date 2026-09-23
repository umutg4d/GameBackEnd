"""User model."""

import uuid

from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # UUID as string
    idfv = db.Column(db.String(50), unique=True)
    vip_status = db.Column(db.Boolean, default=False)
    no_ads_status = db.Column(db.Boolean, default=False)
    soft_currency = db.Column(db.Integer, default=0)
    hint_count = db.Column(db.Integer, default=0)
    match_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'))
    updated_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    # Relationships
    user_categories = db.relationship('UserCategory', back_populates='user')
    user_category_images = db.relationship('UserCategoryImage', back_populates='user')
    user_daily_statistics = db.relationship('UserDailyStatistics', back_populates='user')
    user_missions = db.relationship('UserMission', back_populates='user')
    user_progress = db.relationship('UserProgress', back_populates='user')


    def to_dict(self):
        return {
            "userID": self.user_id,
            "idfv": self.idfv,
            "vipStatus": self.vip_status,
            "noAdsStatus": self.no_ads_status,
            "softCurrency": self.soft_currency,
            "hintCount": self.hint_count,
            "matchCount": self.match_count,
            "createdAt": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            "updatedAt": self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            "categories": [category.to_dict() for category in self.user_categories],
            "completed_images": [image.to_dict() for image in self.user_category_images]
        }
