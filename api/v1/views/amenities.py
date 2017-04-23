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
    if amenity_id is None:
        amenities = [
            state.to_json() for state in storage.all("Amenity").values()]
        return jsonify(amenities)

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_json())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id=None):
    '''This is the 'delete_amenity' method.

    Deletes a given Amenity object.
    '''
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    storage.delete(amenity)
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    '''This is the 'create_amenity' method.

    Creates a new Amenity object.
    '''
    try:
        r = request.get_json()
        if 'name' not in r.keys():
            return "Missing name", 400

        amenity = Amenity(**r)
        amenity.save()
        return jsonify(amenity.to_json()), 201

    except:
        return "Not a JSON", 400


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id=None):
    '''This is the 'update_amenity' method.

    Updates a given Amenity object.
    '''
    try:
        r = request.get_json()
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            abort(404)

        for instance in ("id", "created_at", "updated_at"):
            r.pop(instance, None)

        for key, value in r.items():
            setattr(amenity, key, value)

        amenity.save()
        return jsonify(amenity.to_json()), 200

    except:
        return "Not a JSON", 400
