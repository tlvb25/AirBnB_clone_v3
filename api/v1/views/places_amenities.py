#!/usr/bin/python3
"""place Amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    """Retrieve all amenities"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    review_list = []
    amenities = place.amenities
    for reviews in amenities:
        review_list.append(reviews.to_dict())
    return jsonify(review_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_amenity_from_places(place_id, amenity_id):
    """Delete a amenity"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amen_obj = storage.get("Amenity", amenity_id)
    if amen_obj is None:
        abort(404)
    if amen_obj not in place.amenities:
        abort(404)
    place.amenities.remove(amen_obj)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_amenity_places(place_id, amenity_id):
    """Create a amenity"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amen_obj = storage.get("Amenity", amenity_id)
    if amen_obj is None:
        abort(404)
    if amen_obj in place.amenities:
        return jsonify(amen_obj.to_dict()), 200
    place.amenities.append(amen_obj)
    storage.save()
    return jsonify(amen_obj.to_dict()), 201
