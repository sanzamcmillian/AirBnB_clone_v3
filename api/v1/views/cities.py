#!/usr/bin/python3
"""route for handling states objects and operations
"""
from models import storage
from models.state import State
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.city import City
from flasgger.utils import swag_from


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
@swag_from('documentation/city/cities_by_state.yml', methods=['GET'])
def city_by_state(state_id):
    """retrieves alll city objects from a specific state

    Args:
        state_id (_type_): state object
        return: json of all cities in a state or 404 on error
    """
    city_list = []
    state_obj = storage.get(State, state_id)
    
    
    if not state_obj:
        abort(404)
    for obj in state_obj.cities:
        city_list.append(obj.to_dict())
        
    return jsonify(city_list)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
@swag_from('documentation/city/get_city.yml', methods=['GET'])
def city_by_id(city_id):
    """gets a specific city object by ID

    Args:
        city_id (_type_): city object id
        return: city obj with the specified id or error
    """
    fetched_obj = storage.get(City, city_id)
    
    if not fetched_obj:
        abort(404)    
    return jsonify(fetched_obj.to_dict())


@app_views.route("cities/<city_id>", methods=["PUT"], strict_slashes=False)
@swag_from('documentation/city/put_city.yml', methods=['PUT'])
def city_put(city_id):
    """updates specific city object by ID

    Args:
        city_id (_type_): city object ID
        return: city object and 200 on success, or 400 or 404 on failure
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    
    if not request.get_json():
        abort(400, description="Not a JSON")
        
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
    
    
@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
@swag_from('documentation/city/delete_city.yml', methods=['DELETE'])
def city_delete_by_id(city_id):
    """deletes city by id

    Args:
       city_id (_type_): city object id
       return:: empty dict with 200 or 404 if not found
    """
    fetched_obj = storage.get(City, city_id)
        
    if not fetched_obj:
        abort(404)        
    storage.delete(fetched_obj)
    storage.save()
        
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/city/put_city.yml', methods=['PUT'])
def put_city(city_id):
    """Updates city

    Args:
        city_id (_type_): city id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    
    if not request.get_json():
        abort(400, description="Not a JSON")
    
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)