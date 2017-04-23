#!/usr/bin/python3
'''

This is the 'states' module.

states is a new view for State objects.
Handles all default RestFul API actions.

'''
from api.v1.views import (app_views, State, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/states/', methods=['GET'])
def view_all_states():
    '''This is the 'view_all_states' method.

    Lists all State objects.
    '''
    states = [state.to_json() for state in storage.all("State").values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def view_single_state(state_id=None):
    '''This is the 'view_single_state' method.

    Retrieves data on a single given State object.
    '''
    if state_id is None:
        abort(404)

    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    return jsonify(state.to_json())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id=None):
    '''This is the 'delete_state' method.

    Deletes a State object.
    '''
    if state_id is None:
        abort(404)

    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    '''This is the 'create_state' method.

    Creates a State object.
    '''
    try:
        r = request.get_json()
    except:
        return "Not a JSON", 400

    if 'name' not in r.keys():
        return "Missing name", 400

    state = State(**r)
    state.save()
    return jsonify(state.to_json()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id=None):
    '''This is the 'update_state' module.

    Updates a State object.
    '''
    try:
        r = request.get_json()
    except:
        return "Not a JSON", 400

    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    for instance in ("id", "created_at", "updated_at"):
        r.pop(instance, None)

    for key, value in r.items():
        setattr(state, key, value)

    state.save()
    return jsonify(state.to_json()), 200
