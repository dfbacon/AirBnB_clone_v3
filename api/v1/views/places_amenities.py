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
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)

        amenity = [storage.get("Amenity", i) for i in place.amenities]
        return jsonify(amenity)


    @app_views.route('/places/<place_id>/amenities/<amenity_id>/',
                     methods=['DELETE'])
    def delete_place_amenity(place_id=None, amenity_id=None):
        '''This is the 'delete_place_amenity' method.

        Deletes an Amenity object of a given place.
        '''
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)

        if amenity_id is not None:
            for instance in range(len(place.amenities)):
                if place.amenity[instance] == amenity_id:
                    place.amenity.pop(instance)
                    place.save()

        return jsonify({}), 200


    @app_views.route('/places/<place_id>/amenities/<amenity_id>/',
                     methods=['POST'])
    def create_place_amenity(place_id=None, amenity_id=None):
        '''This is the 'create_place_amenity' method.

        Creates a link between an Amenity object and a given place.
        '''
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)

        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            return "Bad amenity", 404

        if amenity_id in [instance for instance in place.amenities]:
            return jsonify(amenity.to_json()), 200

        place.amenities.append(amenity_id)
        place.save()
        return jsonify(amenity.to_json()), 201

else:
    @app_views.route('/places/<place_id>/amenities/', methods=['GET'])
    def view_amenities_in_place(place_id):
        '''This is the 'view_place_amenity' method.

        Recalls all Amenity objects in a given place.
        '''
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)

        amenity = [instance.to_json() for instance in place.amenities]
        return jsonify(amenity)


    @app_views.route('/places/<place_id>/amenities/<amenity_id>/',
                     methods=['DELETE'])
    def delete_place_amenity(place_id=None, amenity_id=None):
        '''This is the 'delete_place_amenity' method.

        Deletes an Amenity object of a place.
        '''
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)

        amenity = storage.get("Amenity", amenity_id)
        if amenity is not None:
            place.amenities.remove(amenity)
            place.save()
            return jsonify(place.amenities), 200

        return jsonify({}), 200


    @app_views.route('/places/<place_id>/amenities/<amenity_id>/',
                     methods=['POST'])
    def create_place_amenity(place_id=None, amenity_id=None):
        '''This is the 'create_place_amenity' method.

        Creates a link between an Amenity object and a given place.
        '''
        place = storage.get("Place", place_id)
        if place is None:
            return "Bad place", 404

        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            return "Bad amenity", 404

        if amenity in place.amenities:
            return jsonify(amenity.to_json()), 200

        place.amenities.append(amenity)
        place.save()
        storage.save()
        return jsonify(amenity.to_json()), 201
