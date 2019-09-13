#!/usr/bin/python3
"""Place API View"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/states/places/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place(city_id):
    """Retrieve all places"""
    places = storage.get("City", city_id)
    if places is None:
        abort(404)
    place_obj = places.places
    place_list = []
    for place in place_obj:
        place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_a_place(place_id):
    """Retrieve a place"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete a place"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    place_obj.delete()
    storage.save()
    storage.reload()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a Place"""
    cities = storage.get("City", city_id)
    if cities is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in request.get_json():
        return jsonify({'error': 'Missing user_id'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    name = request.get_json().get('name')
    user_id = request.get_json().get('user_id')
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    place_obj = City(name=name, city_id=city_id, user_id=user_id)
    place_obj.save()
    return jsonify(place_obj.to_dict()), 201


@app_views.route('/places/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a city"""
    place_obj = storage.get("Place", city_id)
    if place_obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_obj, k, v)
    storage.save()
    return jsonify(place_obj.to_dict())
