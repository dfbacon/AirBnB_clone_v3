#!/usr/bin/python3
'''

This is the 'cities' module.

cities is a new view for City objects.
Handles all defaut RestFul API actions.

'''
from api.v1.views import (app_views, City, storage)
from flask import (abort, jsonify, request)


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def state_all_cities(state_id):
    '''This is the 'state_all_cities' method.

    Returns all City objects linked to a given State.
    '''

@app_views.route("/cities/<city_id>", methods=["GET"])
def one_city(city_id):
    '''This is the 'one_city' method.

    Returns a matching City object.
    '''

@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_one_city(city_id):
    '''This is the 'delete_one_city' method.

    Deletes a single City object.
    '''

@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_one_city(state_id):
    '''This is the 'create_one_city' method.

    Creates a single City object.
    '''

@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_one_city(city_id):
    '''This is the 'update_one_city' method.

    Update a given City object.
    '''
