#!/usr/bin/python3
"""Places view"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_a_places(city_id):
    """Retrieve all places"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = city.places
    p_list = []
    for p in places:
        p_list.append(p.to_dict())
    return jsonify(p_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def places_by_id(place_id):
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
def create_place(city_id):
    """Create a place"""
    state = storage.get("City", city_id)
    if state is None:
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
    place_obj = Place(name=name, user_id=user_id, city_id=city_id)
    place_obj.save()
    return jsonify(place_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_palce(place_id):
    """Updates a place"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(place_obj, k, v)
    storage.save()
    return jsonify(place_obj.to_dict())
