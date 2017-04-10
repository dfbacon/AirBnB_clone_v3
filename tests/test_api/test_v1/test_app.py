#!/usr/bin/python3
'''

This is the 'test_app' module.

test_app is the testing suite for the 'app' module.

'''
import flask
print("HERE")
print("HERE")
import unittest
print("HERE")
from models import storage
print("HERE")
from api.v1.app import app
print("HERE")


class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_404(self):
        rv = self.app.get('/bad')
        self.assertEqual(rv.status_code, 404)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = json.loads(str(rv.get_data(), encoding="utf-8"))
        self.assertEqual(json_format.get("error"), "Not found")


if __name__ == "__main__":
    unittest.main()
