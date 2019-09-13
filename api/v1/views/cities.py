#!/usr/bin/python3
"""City views """
from models.city import City
from models.state import State
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage


app_views.route('/states/<state_id>/cities', methods=['GET'],
                strict_slashes=False)


def get_all_cities(state_id):
    """retrieves all cities of a state"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    city_obj = state.cities
    city_list = []
    for city in city_obj:
        city_list.append(city.to_dict())
    return jsonify(city_list)


app_views.route('/cities/<city_id>', methods=['GET'])


def get_a_city(city_id):
    """get a city object"""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """deletes a city"""
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        return abort(404)
    city_obj.delete()
    storage.save()
    return jsonify({})




app_views.route('/states/<state_id>/cities', methods=['POST'],
                strict_slashes=False)
def creates_city(state_id):
    """creates a city obj"""
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
            setattr(obj, k, v)
    storage.save()
    return jsonify(city_obj.to_dict())
