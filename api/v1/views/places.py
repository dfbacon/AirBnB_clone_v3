#!/usr/bin/python3
'''

This is the 'places' module.

places is a new view for City objects.
Handles all default RestFul API actions.

'''
from api.v1.views import (app_views, Place, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/cities/<city_id>/places/', methods=['GET'])
def view_places_in_city(city_id):
    '''This is the 'view_places_in_city' method.

    Lists all Place objects in a given city.
    '''

@app_views.route('/places/<place_id>/', methods=['GET'])
def view_place(place_id=None):
    '''This is the 'view_place' method.

    Retrieves data on a given Place object.
    '''

@app_views.route('/places/<place_id>/', methods=['DELETE'])
def delete_place(place_id=None):
    '''This is the 'delete_place' method.

    Deletes a Place object.
    '''

@app_views.route('/cities/<city_id>/places/', methods=['POST'])
def create_place(city_id):
    '''This is the 'create_place' method.

    Creates a Place object.
    '''

@app_views.route('/places/<place_id>/', methods=['PUT'])
def update_place(place_id=None):
    '''This is the 'update_place' method.

    Updates a give Place object.
    '''
