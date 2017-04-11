#!/usr/bin/python3
'''

This is the 'app' module.

app is the first step in the hbhb API development. Sets the first endpoint to
return the status of the API.

'''
from api.v1.views import app_views
from flask import Blueprint, Flask, jsonify, make_response
from flask_cors import CORS, cross_origin
from models import storage
from os import getenv


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    '''This is the 'not_found' method.

    Creates JSON 404 page.
    '''
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown(exception):
    '''This is the 'teardown' method.

    Closes a given session.
    '''
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    print(app.url_map)
    app.run(host=host, port=port)
