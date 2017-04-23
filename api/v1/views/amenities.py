#!/usr/bin/python3
'''

This is the 'amenities' module.

amenities is a new view for Amenity objects.
Handles all default RestFul API actions.

'''
from api.v1.views import (app_views, Amenity, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/amenities/', methods=['GET'])
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def view_amenity(amenity_id=None):
    '''This is the 'amenity_id' method.

    Retrieves a given Amenity object.
    '''

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id=None):
    '''This is the 'delete_amenity' method.

    Deletes a given Amenity object.
    '''

@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    '''This is the 'create_amenity' method.

    Creates a new Amenity object.
    '''

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id=None):
    '''This is the 'update_amenity' method.

    Updates a given Amenity object.
    '''
