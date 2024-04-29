#!/usr/bin/python3
""" Creates a flask app; app_views """

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """ eturns JSON """
    response = {'status': "OK"}
    return jsonify(response) 
