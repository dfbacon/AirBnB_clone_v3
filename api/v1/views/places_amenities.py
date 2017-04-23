#!/usr/bin/python3
'''

This is the 'places_amenities' module.

places_amenities is a new view for the connection between Place and Amenity
objects.

Handles all default API actions.

'''
from api.v1.views import (app_views, Place, storage)
from flask import (abort, jsonify, make_response, request)
from os import getenv
from sqlalchemy import inspect

if getenv('HBNB_TYPE_STORAGE', 'fs') != 'db':

    @app_views.route('/places/<place_id>/amenities/', methods=['GET'])
    def view_place_amenity(place_id):
        '''This is the 'view_place_amenity' method.

        Recalls all Amenity objects in a given place.
        '''

    @app_views.route('/places/<place_id>/amenities/<amenity_id>/',
                     methods=['DELETE'])
    def delete_place_amenity(place_id=None, amenity_id=None):
        '''This is the 'delete_place_amenity' method.

        Deletes an Amenity object of a given place.
        '''

    @app_views.route('/places/<place_id>/amenities/<amenity_id>/',
                     methods=['POST'])
    def create_place_amenity(place_id=None, amenity_id=None):
        '''This is the 'create_place_amenity' method.

        Creates a link between an Amenity object and a given place.
        '''

else:
    @app_views.route('/places/<place_id>/amenities/', methods=['GET'])
    def view_amenities_in_place(place_id):
        '''This is the 'view_place_amenity' method.

        Recalls all Amenity objects in a given place.
        '''

    @app_views.route('/places/<place_id>/amenities/<amenity_id>/',
                     methods=['DELETE'])
    def delete_place_amenity(place_id=None, amenity_id=None):
        '''This is the 'delete_place_amenity' method.

        Deletes an Amenity object of a place.
        '''

    @app_views.route('/places/<place_id>/amenities/<amenity_id>/',
                     methods=['POST'])
    def create_place_amenity(place_id=None, amenity_id=None):
        '''This is the 'create_place_amenity' method.

        Creates a link between an Amenity object and a given place.
        '''
