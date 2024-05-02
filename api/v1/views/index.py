#!/usr/bin/python3
from flask import jsonify
from models import storage
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.review import Review
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """status route
       return: response to json
    """
    return jsonify({"status": "OK"})

@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """stats of all objs route
       return: json of all objs
    """
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    
    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])
    
    return jsonify(num_objs)
