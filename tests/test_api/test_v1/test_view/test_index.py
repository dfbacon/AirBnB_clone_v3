#!/usr/bin/python3
'''

This is the 'test_index' module.

test_index is the testing suite for the 'index' module.

'''
from api.v1.app import (app)
import flask
import json
from models import storage
import unittest


def get_json(response):
    '''This is the 'get_json' method.

    Requests a JSON object from a flask response object.
    '''
    return json.loads(str(response.get_data(), encoding="utf-8"))


class TestIndexView(unittest.TestCase):
    '''This is the 'TestIndexView' class.

    Contains tests for the 'index' module.
    '''

    @classmethod
    def setUpClass(cls):
        '''This is the 'setUpClass' method.

        Set up for testing.
        '''
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.path = "/api/v1"

    def test_status(self):
        '''This is the 'test_status' method.

        Tests for the 'status' method.
        '''
        rv = self.app.get('{}/status/'.format(self.path))
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("status"), "OK")

    def test_stats(self):
        '''This is the 'test_stats' method.

        Tests for the 'stats' method.
        '''
        rv = self.app.get('{}/stats/'.format(self.path))
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        for e in (
                "users", "reviews", "cities", "states", "places", "amenities"):
            self.assertIn(e, json_format.keys())


if __name__ == "__main__":
    unittest.main()
