#!/usr/bin/python3
""" A Flask API """
import flask from Flask
from flask_cors import CORS
from os import getenv
from models import storage
from api.v1.views import api_views

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

""" Register blueprints """
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ Method to handle teardown_appcontext """
    storage.close() 

@app.errorhandler(404)
def handle_404(exception):
    """handles 404 erro

    Args:
        exception (_type_): param.
        return: returns 404 json
    """
    data = {
        "error": "Not found"
    }
    
    resp = jsonify(data)
    resp.status_code = 404
    
    return(resp)

if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
