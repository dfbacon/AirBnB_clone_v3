#!/usr/bin/python3
'''

This is the 'app' module.

app is the first step in the hbhb API development. Sets the first endpoint to
return the status of the API.

'''
from api.v1.views import app_views
from flask import (Blueprint, Flask, jsonify, make_response)
from flask_cors import (CORS, cross_origin)
from models import storage
from os import getenv


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)
