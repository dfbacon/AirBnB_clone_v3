#!/usr/bin/python3
'''

This is the 'places' module.

places is a new view for City objects.
Handles all default RestFul API actions.

'''
from api.v1.views import (app_views, Place, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/cities/<city_id>/places/', methods=['GET'])
def view_places(city_id):
    '''This is the 'view_places' method.

    Lists all Place objects in a given city.
    '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    places = [place.to_json() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>/', methods=['GET'])
def view_single_place(place_id=None):
    '''This is the 'view_single_place' method.

    Retrieves data on a given Place object.
    '''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_json())


@app_views.route('/places/<place_id>/', methods=['DELETE'])
def delete_place(place_id=None):
    '''This is the 'delete_place' method.

    Deletes a Place object.
    '''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places/', methods=['POST'])
def create_place(city_id):
    '''This is the 'create_place' method.

    Creates a Place object.
    '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    try:
        r = request.get_json()

    except:
        return "Not a JSON", 400

    if 'user_id' not in r.keys():
        return "Missing user_id", 400

    user = storage.get("User", r["user_id"])
    if user is None:
        abort(404)

    if 'name' not in r.keys():
        return "Missing name", 400

    r["city_id"] = city_id
    place = Place(**r)
    place.save()
    return jsonify(place.to_json()), 201


@app_views.route('/places/<place_id>/', methods=['PUT'])
def update_place(place_id=None):
    '''This is the 'update_place' method.

    Updates a give Place object.
    '''
