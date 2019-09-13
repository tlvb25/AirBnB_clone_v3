#!/usr/bin/python3
"""Place reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieve all review"""
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    reviews = place.reviews
    review_list = []
    for rev in reviews:
        review_list.append(rev.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def review_by_id(review_id):
    """Retrieve a review"""
    rev_obj = storage.get("Review", review_id)
    if rev_obj is None:
        abort(404)
    return jsonify(rev_obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a review"""
    rev_obj = storage.get("Review", review_id)
    if rev_obj is None:
        abort(404)
    rev_obj.delete()
    storage.save()
    storage.reload()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a review"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in request.get_json():
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get("User", request.get_json().get('user_id'))
    if user is None:
        abort(404)
    user_id = request.get_json().get('user_id')
    if 'text' not in request.get_json():
        return jsonify({'error': 'Missing text'}), 400
    text = request.get_json().get('text')
    rev_obj = Review(text=text, place_id=place_id, user_id=user_id)
    rev_obj.save()
    return jsonify(rev_obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a review"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    rev_obj = storage.get("Review", review_id)
    if rev_obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(rev_obj, k, v)
    storage.save()
    return jsonify(rev_obj.to_dict())
