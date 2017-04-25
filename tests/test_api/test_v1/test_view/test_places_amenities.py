#!/usr/bin/python3
'''

This is the 'test_places_amenities' module.

test_places_amenities is the testing suite for the 'place_amenities' module.

'''
from api.v1.app import (app)
import flask
import json
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
import os
import unittest


def get_json(response):
    '''This is the 'get_json' method.

    Requests a JSON object from a flask response object.
    '''
    return json.loads(str(response.get_data(), encoding="utf-8"))


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') != 'db', "db")
class TestPlaceAmenityView(unittest.TestCase):
    '''This is the 'TestPlaceAmenityView' class.

    Holds all the tests for the 'place_amenity' module.
    '''

    @classmethod
    def setUpClass(cls):
        '''This is the 'setUpClass' method.

        Initializes the testing suite.
        '''
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.path = "/api/v1"
        cls.state_args = {"name": "TestState", "id": "TS"}
        cls.state = State(**cls.state_args)
        cls.state.save()

        cls.city_args = {"name": "TestCity", "id": "TC",
                         "state_id": cls.state.id}
        cls.city = City(**cls.city_args)
        cls.city.save()

        cls.user_args = {"email": "test@test.com", "password": "test",
                         "id": "T1"}
        cls.user = User(**cls.user_args)
        cls.user.save()

        cls.place_args = {"name": "test", "city_id": cls.city.id,
                          "user_id": cls.user.id, "id": "TP"}
        cls.place = Place(**cls.place_args)
        cls.place.save()

        cls.amenity_args = {"name": "testName"}
        cls.amenity = Amenity(**cls.amenity_args)
        cls.amenity.save()
        cls.place.amenities.append(cls.amenity)
        cls.place.save()

    @classmethod
    def tearDownClass(cls):
        '''This is the 'tearDownClass' method

        Tear down of the testing suite
        '''
        storage.delete(cls.state)
        storage.delete(cls.user)

    def test_view_place_amenity(self):
        '''This is the 'test_view_place_amenity' method.

        Tests the 'view_place_amenity' method.
        '''
        rv = self.app.get('{}/places/{}/amenities/'.format(
            self.path, self.place.id), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertTrue(type(json_format), list)
        self.assertIn(self.amenity_args["name"],
                      [e.get("name") for e in json_format])
        self.assertIn(self.amenity.id,
                      [e.get("id") for e in json_format])

    def test_view_pla_place_error(self):
        '''This is the 'test_view_pla_place_error' method.

        Tests the 'view_place_amenity' method with invalid place_id.
        '''
        rv = self.app.get('{}/places/{}/amenities/'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_delete_pla_amentiy(self):
        '''This is the 'test_delete_pla_amentiy' method.

        Tests the 'delete_place_amenity' method for deleting an amenity.
        '''
        amenity_args = {"name": "testA", "id": "TA"}
        amenity = Amenity(**amenity_args)
        self.place.amenities.append(amenity)
        amenity.save()

        rv = self.app.delete('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, "TA"), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format, {})
        self.assertIsNotNone(storage.get("Amenity", amenity.id))
        storage.delete(amenity)

    def test_delete_pla_pid_error(self):
        '''This is the 'test_delete_pla_pid_error' method.

        Tests the 'delete_place_amenity' method with an invalid place_id.
        '''
        rv = self.app.delete('{}/places/{}/amenities/{}/'.format(
            self.path, "noID", self.amenity.id), follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_delete_pla_amenity_error(self):
        '''This is the 'test_delete_pla_amenity_error' method.

        Tests the 'delete_place_amenity' method with a non-matching amenity.
        '''
        rv = self.app.delete('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, "noID"), follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_delete_pla_no_amenity(self):
        '''This is the 'test_delete_pla_no_amenity' method.

        Tests the 'delete_place_amenity' method for an amenity not in a
        given place.
        '''
        amenity_args = {"name": "testA", "id": "TA"}
        amenity = Amenity(**amenity_args)
        amenity.save()

        rv = self.app.delete('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, amenity.id), follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(amenity)

    def test_create_place_amenity(self):
        '''This is the 'test_create_place_amenity' method.

        Tests the 'create_place_amenity' method.
        '''
        amenity_args = {"name": "testA", "id": "TA"}
        amenity = Amenity(**amenity_args)
        amenity.save()

        rv = self.app.post('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, amenity.id), follow_redirects=True)
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), amenity_args["name"])
        self.assertEqual(json_format.get("id"), amenity_args["id"])
        self.assertIn(self.amenity.id, [a.id for a in storage.get(
            "Place", self.place.id).amenities])
        storage.delete(amenity)

    def test_create_pla_existing(self):
        '''This is the 'test_create_pla_existing' method.

        Tests the 'create_place_amenity' method with a pre-existing amenity.
        '''
        rv = self.app.post('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, self.amenity.id), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), self.amenity_args["name"])
        self.assertEqual(json_format.get("id"), self.amenity.id)
        self.assertIn(self.amenity.id, [a.id for a in storage.get(
            "Place", self.place.id).amenities])

    def test_create_pla_place_error(self):
        '''This is the 'test_create_pla_place_error' method.

        Tests the 'create_place_amenity' method with invalid place.
        '''
        amenity_args = {"name": "test", "id": "TA"}
        amenity = Amenity(**amenity_args)
        amenity.save()

        rv = self.app.post('{}/places/{}/amenities/{}/'.format(
            self.path, "noID", amenity.id), follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(amenity)

    def test_create_pla_amenity_error(self):
        '''This is the 'test_create_pla_amenity_error' method.

        Tests the 'create_place_amenity' method with invalid amenity.
        '''
        amenity_args = {"name": "testA", "id": "TA"}
        amenity = Amenity(**amenity_args)
        amenity.save()

        rv = self.app.post('{}/places/{}/amenities/{}/'.format(
            self.path, self.place.id, "noID"), follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(amenity)


if __name__ == "__main__":
    unittest.main()
