#!/usr/bin/python3
"""route for handling state objects
"""
from models import storage
from flasgger.utils import swag_from
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_state.yml', methods=['GET'])
def state_get_all():
    """retrieves all state objects
       return: json of all states
    """
    state_list = []
    state_obj = storage.all(State).values()
    for state in state_obj:
        state_list.append(state.to_dict())    
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_id_state.yml', methods=['get'])
def state_by_id(state_id):
    """gets a specific state object by ID

    Args:
        state_id (_type_): state object id
        return: state obj with the specified id or erro
    """
    fetched_obj = storage.get(State, state_id)
    
    if not fetched_obj:
        abort(404)    
    return jsonify(fetched_obj.to_dict())


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
@swag_from('documentation/state/put_state.yml', methods=['PUT'])
def state_put(state_id):
    """updates specific state object ID

    Args:
        state_id (_type_): state object ID
        return: state object and 200 on success, or 400,404 on failure
    """
    state = storage.get(State, state_id)
    
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
        
    ignore = ['id', 'created_at', 'updated_at']
    
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(State, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
@swag_from('documentation/state/post_state.yml', methods=['POST'])
def state_delete_by_id(state_id):
    """deletes State by id

    Args:
        state_id (_type_): state object id
        return: empty dict with 200 or 404 if not found
    """
    
    fetched_obj = storage.get(State, state_id)
    
    if not fetched_obj:
        abort(404)
        
    storage.delete(fetched_obj)
    storage.save()
    
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/post_state.yml', methods=['POST'])
def post_state():
    """creates a state
    """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
        
    data = request.get_json()
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)