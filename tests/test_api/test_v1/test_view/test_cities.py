#!/usr/bin/python3
'''

This is the 'test_cities' module.

test_cities is the testing suite for the 'cities' module.

'''
from api.v1.app import (app)
import flask
import json
from models import storage
from models.city import City
from models.state import State
import unittest


def get_json(response):
    '''This is the 'get_json' method.

    Requests a JSON object from a flask response object.
    '''
    return json.loads(str(response.get_data(), encoding="utf-8"))


class TestCityView(unittest.TestCase):
    '''This is the TestCityView class.

    Contains all tests for the 'cities' module.
    '''

    @classmethod
    def setUpClass(cls):
        '''This is the 'setUpClass' method.

        Set up testing suite.
        '''
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.path = "/api/v1"
        cls.state_args = {"name": "Test", "id": "TS"}
        cls.state = State(**cls.state_args)
        cls.state.save()

    @classmethod
    def tearDownClass(cls):
        '''This is the 'teadDownClass' method.

        Tear down testing suite.
        '''
        storage.delete(cls.state)

    def test_all_cities(self):
        '''This is the 'test_all_cities' method.

        Tests for the 'all_cities' method.
        '''
        city_args = {"name": "TestCity", "id": "TC", "state_id": "TS"}
        city = City(**city_args)
        city.save()

        rv = self.app.get('{}/states/{}/cities'.format(
            self.path, self.state.id), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertTrue(type(json_format), list)
        self.assertIn(city_args["name"], [e.get("name") for e in json_format])
        storage.delete(city)

    def test_all_cities_state_error(self):
        '''This is the 'test_all_cities_state_error' method.

        Tests for the 'all_cities' method, passing a bad state_id.
        '''
        city_args = {"name": "TestBad", "id": "TB", "state_id": "TS"}
        city = City(**city_args)
        city.save()

        rv = self.app.get('{}/states/{}'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(city)

    def test_one_city(self):
        '''This is the 'test_one_city' method.

        Tests the 'one_city' method.
        '''
        city_args = {"name": "TestCity", "id": "TC", "state_id": "TS"}
        city = City(**city_args)
        city.save()

        rv = self.app.get('{}/cities/{}'.format(self.path, city_args["id"]),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), city_args["name"])
        self.assertEqual(json_format.get("id"), city_args["id"])
        storage.delete(city)

    def test_one_city_error(self):
        '''This is the 'test_one_city_error' method.

        Tests the 'one_city' method, passing a non-matching id.
        '''
        city_args = {"name": "TestCity", "id": "TC", "state_id": "TS"}
        city = City(**city_args)
        city.save()

        rv = self.app.get('{}/cities/{}/'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(city)

    def test_delete_one_city(self):
        '''This is the 'test_delete_city' method.

        Tests the 'delete_one_city' method.
        '''
        city_args = {"name": "TestCity", "id": "TC", "state_id": "TS"}
        city = City(**city_args)
        city.save()

        rv = self.app.delete('{}/cities/{}/'.format(
            self.path, city_args["id"]), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format, {})
        self.assertIsNone(storage.get("City", city_args["id"]))

    def test_delete_one_city_error(self):
        '''This is the 'test_delete_one_city_error' method.

        Tests the 'delete_one_city' method, passing a non-matching id.
        '''
        city_args = {"name": "TestCity", "id": "TC", "state_id": "TS"}
        city = City(**city_args)
        city.save()

        rv = self.app.delete('{}/cities/{}/'.format(
            self.path, "noID"), follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(city)

    def test_create_city(self):
        '''This is the 'test_create_one_city' method.

        Tests the 'create_one_city' method.
        '''
        city_args = {"name": "TestCity", "id": "TC"}

        rv = self.app.post('{}/states/{}/cities/'.format(self.path,
                                                         self.state.id),
                           content_type="application/json",
                           data=json.dumps(city_args), follow_redirects=True)
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), city_args["name"])
        self.assertEqual(json_format.get("id"), city_args["id"])

        s = storage.get("City", city_args["id"])
        self.assertIsNotNone(s)
        storage.delete(s)

    def test_create_one_city_json_error(self):
        '''This is the 'test_create_one_city_json_error' method.

        Tests the 'create_one_city' method with invalid JSON.
        '''
        city_args = {"name": "TestCity", "id": "TC"}

        rv = self.app.post('{}/states/{}/cities/'.format(self.path,
                                                         self.state.id),
                           content_type="application/json",
                           data=city_args, follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")

    def test_create_one_city_name_error(self):
        '''This is the 'test_create_one_city_name_error' method.

        Tests the 'create_one_city' method with missing name value.
        '''
        city_args = {"id": "TC2"}

        rv = self.app.post('{}/states/{}/cities/'.format(self.path,
                                                         self.state.id),
                           content_type="application/json",
                           data=json.dumps(city_args), follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Missing name")

    def test_create_one_city_sid_error(self):
        '''This is the 'test_create_one_city_sid_error' method.

        Tests the 'create_one_city' method with non-matching state_id.
        '''
        city_args = {"name": "TestCity", "id": "TB2"}

        rv = self.app.post('{}/states/{}/cities/'.format(self.path, "noID"),
                           content_type="application/json",
                           data=json.dumps(city_args), follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_update_one_city_name(self):
        '''This is the 'test_update_one_city_name' method.

        Tests for updating the name of a City object using the
        'update_one_city' method.
        '''
        city_args = {"name": "TestCity", "id": "TC", "state_id": "TS"}
        city = City(**city_args)
        city.save()

        rv = self.app.put('{}/cities/{}/'.format(self.path, city.id),
                          content_type="application/json",
                          data=json.dumps({"name": "T"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), "T")
        self.assertEqual(json_format.get("id"), city_args["id"])
        self.assertEqual(json_format.get("state_id"), city_args["state_id"])
        storage.delete(city)

    def test_update_city_id(self):
        '''This is the 'test_update_one_city_id' mehtod.

        Tests for updating the id of a City object using the
        'update_one_city' method.
        '''
        city_args = {"name": "TestCity", "id": "TC", "state_id": "TS"}
        city = City(**city_args)
        city.save()

        rv = self.app.put('{}/cities/{}/'.format(self.path, city.id),
                          content_type="application/json",
                          data=json.dumps({"id": "T"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), city_args["name"])
        self.assertEqual(json_format.get("id"), city_args["id"])
        self.assertEqual(json_format.get("state_id"), city_args["state_id"])
        storage.delete(city)

    def test_update_one_city_sid(self):
        '''This is the 'test_update_one_city_sid' method.

        Tests for updating the state_id of a City object using the
        'update_one_city' method.
        '''
        city_args = {"name": "TestCity", "id": "TC", "state_id": "TS"}
        city = City(**city_args)
        city.save()

        rv = self.app.put('{}/cities/{}/'.format(self.path, city.id),
                          content_type="application/json",
                          data=json.dumps({"state_id": "T"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), city_args["name"])
        self.assertEqual(json_format.get("id"), city_args["id"])
        self.assertEqual(json_format.get("state_id"), city_args["state_id"])
        storage.delete(city)

    def test_update_one_city_state_json(self):
        '''This is the 'test_update_one_city_state_json' method.

        Tests for updating the state_id of a City object with an invalid JSON.
        '''
        city_args = {"name": "TestCity", "id": "TC", "state_id": "TS"}
        city = City(**city_args)
        city.save()

        rv = self.app.put('{}/cities/{}/'.format(self.path, city.id),
                          content_type="application/json",
                          data={"id": "T"},
                          follow_redirects=True)

        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")
        storage.delete(city)

    def test_update_one_city_id_error(self):
        '''This is the 'test_update_one_city_id_error' method

        Tests for updating city_id of a City object with an invalid id.
        '''
        city_args = {"name": "TestCity", "id": "TC", "state_id": "TS"}
        city = City(**city_args)
        city.save()

        rv = self.app.put('{}/cities/{}/'.format(self.path, "noID"),
                          content_type="application/json",
                          data=json.dumps({"name": "T"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(city)


if __name__ == "__main__":
    unittest.main()
