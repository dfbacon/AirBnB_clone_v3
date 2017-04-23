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

@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id=None):
    '''This is the 'delete_user' method.

    Deletes a single User object.
    '''

@app_views.route('/users/', methods=['POST'])
def create_user():
    '''This is the 'create_user' method.

    Creates a new User object.
    '''

@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id=None):
    '''This is the 'update_user' method.

    Updates a User object.
    '''
