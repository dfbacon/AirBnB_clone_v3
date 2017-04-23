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
def view_one_state(state_id=None):
    '''This is the 'view_one_state' method.

    Retrieves data on a single given State object.
    '''

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id=None):
    '''This is the 'delete_state' method.

    Deletes a State object.
    '''

@app_views.route('/states/', methods=['POST'])
def create_state():
    '''This is the 'create_state' method.

    Creates a State object.
    '''

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id=None):
    '''This is the 'update_state' module.

    Updates a State object.
    '''
