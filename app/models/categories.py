"""Category and user-category models."""

from app.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    # Relationships
    category_images = db.relationship('CategoryImage', back_populates='category')
    user_categories = db.relationship('UserCategory', back_populates='category')


class CategoryImage(db.Model):
    __tablename__ = 'category_images'

    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    image_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default='CURRENT_TIMESTAMP')

    # Relationships
    category = db.relationship('Category', back_populates='category_images')
    user_category_images = db.relationship('UserCategoryImage', back_populates='category_image')


class UserCategory(db.Model):
    __tablename__ = 'user_categories'

    user_category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    purchased_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'))

    # Relationships
    user = db.relationship('User', back_populates='user_categories')
    category = db.relationship('Category', back_populates='user_categories')

    def to_dict(self):
        return {
            "category_id": self.category.category_id,
            "name": self.category.name
        }


class UserCategoryImage(db.Model):
    __tablename__ = 'user_category_images'

    user_image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('category_images.image_id'), nullable=False)
    completed_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP'))

    # Relationships
    user = db.relationship('User', back_populates='user_category_images')
    category_image = db.relationship('CategoryImage', back_populates='user_category_images')
