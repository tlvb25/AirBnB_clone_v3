#!/usr/bin/python3
"""City file for views module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city(state_id):
    """Retrieve all cities objects of a state"""
    states = storage.get("State", state_id)
    if states is None:
        abort(404)
    city_obj = states.cities
    city_list = []
    for city in city_obj:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_by_id(city_id):
    """Retrieve a city object by id"""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete a city object by id"""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    city_obj.delete()
    storage.save()
    storage.reload()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a city object"""
    states = storage.get("State", state_id)
    if states is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    name = request.get_json().get('name')
    city_obj = City(name=name, state_id=state_id)
    city_obj.save()
    return jsonify(city_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a city object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(city_obj, k, v)
    storage.save()
    return jsonify(city_obj.to_dict())
