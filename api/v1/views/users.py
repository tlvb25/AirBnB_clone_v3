#!/usr/bin/python3
"""User api View"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_user():
    """Retrieve all users"""
    user_list = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a user"""
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user"""
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    user_obj.delete()
    storage.save()
    storage.reload()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a user"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    user_dict = request.get_json()
    user_obj = User(**user_dict)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a user"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user_obj, k, v)
    storage.save()
    return jsonify(user_obj.to_dict())
