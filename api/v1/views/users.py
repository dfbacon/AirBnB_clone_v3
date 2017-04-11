#!/usr/bin/python3
'''

This is the 'users' module.

users is a new view for User objects.
Handles all default RestFul API actions.

'''
from api.v1.views import (app_views, User, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/users/', methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'])
def view_user(user_id=None):
    '''This is the 'user_id' method.

    Retrieves a User object.
    '''
    if user_id is None:
        users = [state.to_json() for state in storage.all("User").values()]
        return jsonify(users)

    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id=None):
    '''This is the 'delete_user' method.

    Deletes a single User object.
    '''
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    storage.delete(user)
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    '''This is the 'create_user' method.

    Creates a new User object.
    '''
    try:
        r = request.get_json()
    except:
        r = None

    if r is None:
        return "Not a JSON", 400
    if 'email' not in r.keys():
        return "Missing email", 400
    if 'password' not in r.keys():
        return "Missing password", 400

    user = User(**r)
    user.save()
    return jsonify(user.to_json()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id=None):
    '''This is the 'update_user' method.

    Updates a User object.
    '''
    try:
        r = request.get_json()
    except:
        r = None

    if r is None:
        return "Not a JSON", 400

    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    for instance in ("id", "email", "created_at", "updated_at"):
        r.pop(instance, None)

    for key, value in r.items():
        setattr(user, key, value)

    user.save()
    return jsonify(a.to_json()), 200
