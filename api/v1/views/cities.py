#!/usr/bin/python3
'''

This is the 'cities' module.

cities is a new view for City objects.
Handles all defaut RestFul API actions.

'''
from api.v1.views import (app_views, City, storage)
from flask import (abort, jsonify, request)


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def all_cities(state_id):
    '''This is the 'all_cities' method.

    Returns all City objects linked to a given State.
    '''
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    cities = [city.to_json() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"])
def one_city(city_id):
    '''This is the 'one_city' method.

    Returns a matching City object.
    '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_json())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_one_city(city_id):
    '''This is the 'delete_one_city' method.

    Deletes a single City object.
    '''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_one_city(state_id):
    '''This is the 'create_one_city' method.

    Creates a single City object.
    '''
    try:
        r = request.get_json()
    except:
        return "Not a JSON", 400

    if 'name' not in r.keys():
        return "Missing name", 400

    city = City(**r)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_json()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_one_city(city_id):
    '''This is the 'update_one_city' method.

    Update a given City object.
    '''
