#!/usr/bin/python3
'''

This is the 'index' module.

index is part of the first step in the hbhb API development.
It holds the endpoint.

'''

from api.v1.views import app_views, storage
from flask import jsonify


@app_views.route('/status')
def status():
    '''This is the 'status' method.
    Returns status as "OK"
    '''
    return jsonify({"status": "OK"})
