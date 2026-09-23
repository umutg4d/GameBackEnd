"""Category access and image-completion endpoints."""

import flask
from flask import Blueprint, abort, jsonify

from app.api.validation import validate_query_input
from app.extensions import db
from app.models import User, UserCategory, UserCategoryImage
from app.schemas.requests import CamelCaseUserRequest, CompleteImageRequest, OpenCategoryRequest


categories_blueprint = Blueprint("categories", __name__)


@categories_blueprint.get("/get-user-categories")
@validate_query_input(CamelCaseUserRequest)
def get_user_categories():
    if 'userId' in flask.request.args:
        user_id = flask.request.args.get('userId')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "User ID is required"}))

    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
        abort(404, description="User not found")

    return jsonify(dict({"status": "success", "categories": [category.to_dict() for category in user.user_categories]}))


@categories_blueprint.get("/get-completed-images")
@validate_query_input(CamelCaseUserRequest)
def get_completed_images():
    if 'userId' in flask.request.args:
        user_id = flask.request.args.get('userId')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "User ID is required"}))

    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
        abort(404, description="User not found")

    return jsonify(dict({"status": "success", "categories": [image.to_dict() for image in user.user_category_images]}))


@categories_blueprint.post("/open-category")
@validate_query_input(OpenCategoryRequest)
def open_category():
    if 'user_id' in flask.request.args:
        user_id = flask.request.args.get('user_id')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "User ID is required"}))
    
    if 'category_id' in flask.request.args:
        category_id = flask.request.args.get('category_id')
    else:
        print("Category ID is required")
        return jsonify(dict({"status": False, "message": "Category ID is required"}))

    user_category = UserCategory(user_id=user_id, category_id=category_id)
    db.session.add(user_category)
    db.session.commit()

    return jsonify(dict({"status": True, "message": "Opened category successfully"}))


@categories_blueprint.post("/complete-image")
@validate_query_input(CompleteImageRequest)
def complete_image():
    if 'user_id' in flask.request.args:
        user_id = flask.request.args.get('user_id')
    else:
        print("User ID is required")
        return jsonify(dict({"status": False, "message": "User ID is required"}))
    
    if 'image_id' in flask.request.args:
        image_id = flask.request.args.get('image_id')
    else:
        print("Image ID is required")
        return jsonify(dict({"status": False, "message": "Image ID is required"}))

    user_category_image = UserCategoryImage(user_id=user_id, image_id=image_id)
    db.session.add(user_category_image)
    db.session.commit()

    return jsonify(dict({"status": True, "message": "Completed the image successfully"}))
