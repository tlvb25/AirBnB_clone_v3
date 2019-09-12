from models.state import State
from flask import jsonify, abort, request, Flask
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    all_states = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(all_states)

@app_views.route('/states/<state_id>', methods=['GET'])
def get_a_state(state_id):
    """retrieves state by state id"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_obj(state_id):
    """deletes a state object"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_State():
    if not request.get_json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    dic = request.get_json()
    obj = State(**dic)
    obj.save()
    return jsonify(obj.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    obj = get("State", state_id)
    if obj is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': "Not a Json"}), 400
    for k, v in request.get_json().items():
        if not hasattr[k, 'id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict())
