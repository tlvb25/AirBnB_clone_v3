#!/usr/bin/python3
"""" amenity.py"""
from models.amenity import Amenity
from flask import jsonify, abort, request, Flask
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """retrieves all amenity obj"""
    all_amenities = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(all_amenities)

@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_an_amenity(amenity_id):
    """retrieves amenity by id"""
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_obj(amenity_id):
    """deletes a amenity object"""
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_Amenity():
    """create a Amenity obj"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    dic = request.get_json()
    obj = Amenity(**dic)
    obj.save()
    return jsonify(obj.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """updates Amenity object"""
    if not request.get_json():
        return jsonify({'error': "Not a Json"}), 400
    obj = storage.get("Amenity", state_id)
    if obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict())
