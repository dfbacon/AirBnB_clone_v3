#!/usr/bin/python3
'''

This is the 'index' module.

index is part of the first step in the hbhb API development.
It holds the endpoint.

'''

from api.v1.views import app_views, storage
from flask import jsonify


@app_views.route('/status/')
def status():
    '''This is the 'status' method.

    Returns status as "OK"
    '''
    return jsonify({"status": "OK"})


@app_views.route('/stats/')
def stats():
    '''This is the 'stats' method.

    Counts the number of objects by type.
    '''

    valid_models = {"Amenity": "amenities", "City": "cities",
                    "Place": "places", "Review": "reviews", "State": "states",
                    "User": "users"}
    counts = {}
    for cls in valid_models.keys():
        counts[valid_models[cls]] = storage.count(cls)
    return jsonify(counts)
