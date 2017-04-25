#!/usr/bin/python3
'''

This is the 'test_app' module.

test_app is the testing suite for the 'app' module.

'''
from api.v1.app import app
import flask
import json
from models import storage
import unittest


class TestApp(unittest.TestCase):
    '''This is the 'TestApp' class.

    Testing suite for the 'app' module.
    '''
    @classmethod
    def setUpClass(self):
        '''This is the 'setUpClass' method.

        Initializes the testing suite.
        '''
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_404(self):
        '''This is the 'test_404' method.

        Tests the 'not_found' method.
        '''
        rv = self.app.get('/bad')
        self.assertEqual(rv.status_code, 404)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = json.loads(str(rv.get_data(), encoding="utf-8"))
        self.assertEqual(json_format.get("error"), "Not found")


if __name__ == "__main__":
    unittest.main()
