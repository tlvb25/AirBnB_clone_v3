#!/usr/bin/python3
"""State file for views module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all():
    """Retrieve all amenity objects"""
    amen_list = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(amen_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenty(amenity_id):
    """Retrieve an amenity object by id"""
    amen_obj = storage.get("Amenity", amenity_id)
    if amen_obj is None:
        abort(404)
    return jsonify(amen_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_a_amenity(amenity_id):
    """Delete an amenity object by id"""
    amen_obj = storage.get("Amenity", amenity_id)
    if amen_obj is None:
        abort(404)
    amen_obj.delete()
    storage.save()
    storage.reload()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create an amenity object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    name = request.get_json().get('name')
    amen_obj = Amenity(name=name)
    amen_obj.save()
    return jsonify(amen_obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an amenity object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    amen_obj = storage.get("Amenity", amenity_id)
    if amen_obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amen_obj, k, v)
    storage.save()
    return jsonify(amen_obj.to_dict())
