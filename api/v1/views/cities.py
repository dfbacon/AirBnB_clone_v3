#!/usr/bin/python3
'''

This is the 'cities' module.

cities is a new view for City objects.
Handles all defaut RestFul API actions.

'''
from api.v1.views import (app_views, City, storage)
from flask import (abort, jsonify, request)


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def all_cities(state_id):
    '''This is the 'all_cities' method.

    Returns all City objects linked to a given State.
    '''
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    cities = [city.to_json() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def one_city(city_id):
    '''This is the 'one_city' method.

    Returns a matching City object.
    '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_json())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_one_city(city_id):
    '''This is the 'delete_one_city' method.

    Deletes a single City object.
    '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_one_city(state_id):
    '''This is the 'create_one_city' method.

    Creates a single City object.
    '''
    try:
        r = request.get_json()
    except:
        r = None

    if r is None:
        return "Not a JSON", 400
    if 'name' not in r.keys():
        return "Missing name", 400

    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    city = City(**r)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_json()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_one_city(city_id):
    '''This is the 'update_one_city' method.

    Update a given City object.
    '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    try:
        r = request.get_json()
    except:
        r = None

    if r is None:
        return "Not a JSON", 400

    for instance in ("id", "created_at", "updated_at", "state_id"):
        r.pop(instance, None)

    for key, value in r.items():
        setattr(city, key, value)

    city.save()
    return jsonify(city.to_json()), 200
