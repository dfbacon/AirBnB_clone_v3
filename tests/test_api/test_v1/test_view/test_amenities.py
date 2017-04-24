#!/usr/bin/python3
'''

This is the 'test_amenities' module.

test_amenities is the testing suite for the 'amenities' module.

'''
from api.v1.app import (app)
import flask
import json
from models import storage
from models.amenity import Amenity
import unittest


def get_json(response):
    '''This is the 'get_json' method.

    Requests a JSON object from a flask response object.
    '''
    return json.loads(str(response.get_data(), encoding="utf-8"))


class TestAmenity(unittest.TestCase):
    '''This is the TestAmenity class.

    Contains tests for the 'amenities' mdoule.
    '''

    @classmethod
    def setUpClass(cls):
        '''This is the 'setUpClass' method.

        Set up for testing.
        '''
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.path = "/api/v1"

    def test_view_amenity(self):
        '''This is the 'test_view_amenity' method.

        Tests for the 'view_amenity' method.
        '''
        amenity_args = {"name": "test"}
        amenity = Amenity(**amenity_args)
        amenity.save()

        rv = self.app.get('{}/amenities/'.format(self.path),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = getJson(rv)
        self.assertTrue(type(json_format), list)
        self.assertIn(
            amenity_args["name"], [e.get("name") for e in json_format])
        storage.delete(amenity)

    def test_view_single_amenity(self):
        '''This is the 'test_view_single_amenity' method.

        Tests for retrieving one Amenity object.
        '''
        amenity_args = {"name": "test", "id": "TS2"}
        amenity = Amenity(**amenity_args)
        amenity.save()

        rv = self.app.get('{}/amenities/{}'.format(
            self.path, amenity_args["id"]), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), amenity_args["name"])
        self.assertEqual(json_format.get("id"), amenity_args["id"])
        storage.delete(amenity)

    def test_view_single_amenity_error(self):
        '''This is the 'test_view_single_amenity_error' method.

        Tests for retrieving one Amenity object with incorrect id.
        '''
        amenity_args = {"name": "test", "id": "TS1"}
        amenity = Amenity(**amenity_args)
        amenity.save()

        rv = self.app.get('{}/amenities/{}'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(amenity)

    def test_delete_amenity(self):
        '''This is the 'test_delete_amenity' method.

        Tests for deleting an Amenity object.
        '''
        amenity_args = {"name": "test", "id": "TS"}
        amenity = Amenity(**amenity_args)
        amenity.save()

        rv = self.app.delete('{}/amenities/{}/'.format(
            self.path, amenity_args["id"]),
                                   follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = getJson(rv)
        self.assertEqual(json_format, {})
        self.assertIsNone(storage.get("Amenity", amenity_args["id"]))

    def test_delete_amenity_error(self):
        '''This is the 'test_delete_amenity_error' method.

        Tests for deleting an Amenity object with an incorrect id.
        '''
        amenity_args = {"name": "test", "id": "TS"}
        amenity = Amenity(**amenity_args)
        amenity.save()

        rv = self.app.delete('{}/amenities/{}/'.format(self.path, "noID"),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(amenity)

    def test_create_amenity(self):
        '''This is the 'test_create_amenity' method.

        Tests for creating an Amenity object.
        '''
        amenity_args = {"name": "test", "id": "TS"}

        rv = self.app.post('{}/amenities/'.format(self.path),
                           content_type="application/json",
                           data=json.dumps(amenity_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), amenity_args["name"])
        self.assertEqual(json_format.get("id"), amenity_args["id"])

        s = storage.get("Amenity", amenity_args["id"])
        self.assertIsNotNone(s)
        storage.delete(s)

    def test_create_amenity_json_error(self):
        '''This is the 'test_create_amenity_json_error' method.

        Tests for creating an Amenity object with an incorrect id.
        '''
        amenity_args = {"name": "test", "id": "TS"}

        rv = self.app.post('{}/amenities/'.format(self.path),
                           content_type="application/json",
                           data=amenity_args,
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")

    def test_create_amenity_name_error(self):
        '''This is the 'test_create_amenity_name_error' method.

        Tests for creating an Amenity object with a missing name.
        '''
        amenity_args = {"id": "TS2"}

        rv = self.app.post('{}/amenities/'.format(self.path),
                           content_type="application/json",
                           data=json.dumps(amenity_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Missing name")

    def test_update_amenity_name(self):
        '''This is the 'test_update_amenity_name' method.

        Tests for updating the name of an Amenity object.
        '''
        amenity_args = {"name": "test", "id": "TS1"}
        amenity = Amenity(**amenity_args)
        amenity.save()

        rv = self.app.put('{}/amenities/{}/'.format(self.path, amenity.id),
                          content_type="application/json",
                          data=json.dumps({"name": "T"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), "T")
        self.assertEqual(json_format.get("id"), amenity_args["id"])
        storage.delete(amenity)

    def test_update_amenity_id(self):
        '''This is the 'test_update_amenity_id' method.

        Tests for updating the id of an Amenity object.
        '''
        amenity_args = {"name": "test", "id": "TS1"}
        amenity = Amenity(**amenity_args)
        amenity.save()

        rv = self.app.put('{}/amenities/{}/'.format(self.path, amenity.id),
                          content_type="application/json",
                          data=json.dumps({"id": "T"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), amenity_args["name"])
        self.assertEqual(json_format.get("id"), amenity_args["id"])
        storage.delete(amenity)

    def test_update_amenity_json_error(self):
        '''This is the 'test_update_amenity_json_error' method.

        Tests for updating an Amenity object with an invalid JSON object.
        '''
        amenity_args = {"name": "test", "id": "TS2"}
        amenity = Amenity(**amenity_args)
        amenity.save()

        rv = self.app.put('{}/amenities/{}/'.format(self.path, amenity.id),
                          content_type="application/json",
                          data={"id": "T"},
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")
        storage.delete(amenity)

    def test_update_amenity_id_error(self):
        '''This is the 'test_update_amenity_id_error' method.

        Tests for updating an Amenity object with an invalid id.
        '''
        amenity_args = {"name": "test", "id": "TS"}
        amenity = Amenity(**amenity_args)
        amenity.save()

        rv = self.app.put('{}/amenities/{}/'.format(self.path, "noID"),
                          content_type="application/json",
                          data=json.dumps({"id": "T"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(amenity)


if __name__ == "__main__":
    unittest.main()
