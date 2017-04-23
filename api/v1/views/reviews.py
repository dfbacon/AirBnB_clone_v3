#!/usr/bin/python3
'''

This is the 'reviews' module.

reviews is a new view for Review objects.
Handles all default RestFul API actions.

'''
from api.v1.views import (app_views, Review, storage)
from flask import (abort, jsonify, request)


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def all_reviews(place_id):
    '''This is the 'all_reviews' method.

    Compiles a list of all Review objects of a given place.
    '''
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    reviews = [review.to_json() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def single_review(review_id):
    '''This is the 'single_review' method.

    Returns a single Review object of a given place.
    '''
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_json())


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_single_review(review_id):
    '''This is the 'delete_single_review' method.

    Deletes a single Review object.
    '''

@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    '''This is the 'create_review' method.

    Creates a Review object of a given place.
    '''

@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    '''This is the 'update_review' method.

    Updates a Review object.
    '''
