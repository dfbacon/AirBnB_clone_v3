#!/usr/bin/python3
'''

This is the 'test_places' module.

test_places is the testing suite for the 'places' module.

'''
from api.v1.app import (app)
import flask
import json
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
import unittest


def get_json(response):
    '''This is the 'get_json' method.

    Requests a JSON object from a flask response object.
    '''
    return json.loads(str(response.get_data(), encoding="utf-8"))


class TestCityView(unittest.TestCase):
    '''This is the 'TestCityView' class.

    Contains all tests for the 'places' module.
    '''

    @classmethod
    def setUpClass(cls):
        '''This is the  'SetUpClass' method.

        Initialize testing suite.
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

    @classmethod
    def tearDownClass(cls):
        storage.delete(cls.state)
        storage.delete(cls.user)

    def test_view_places(self):
        '''This is the 'test_view_places' method.

        Tests the 'view_places' method.
        '''
        place_args = {"name": "test", "city_id": self.city.id,
                      "user_id": self.user.id}
        place = Place(**place_args)
        place.save()

        rv = self.app.get('{}/cities/{}/places'.format(
            self.path, self.city.id),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertTrue(type(json_format), list)
        self.assertIn(place_args["name"], [e.get("name") for e in json_format])
        self.assertIn(place_args["user_id"],
                      [e.get("user_id") for e in json_format])
        storage.delete(place)

    def test_view_places_cid_error(self):
        '''This is the 'test_view_places_cid_error' method.

        Tests the 'view_places' method with an invalid city_id.
        '''
        place_args = {"name": "test", "city_id": self.city.id,
                      "user_id": self.user.id}
        place = Place(**place_args)
        place.save()

        rv = self.app.get('{}/cities/{}/places'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(place)

    def test_view_single_place(self):
        '''This is the 'test_view_single_place' method.

        Tests the 'view_single_place' method.
        '''
        place_args = {"name": "test", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "TT"}
        place = Place(**place_args)
        place.save()

        rv = self.app.get('{}/places/{}'.format(self.path, place_args["id"]),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), place_args["name"])
        self.assertEqual(json_format.get("id"), place_args["id"])
        self.assertEqual(json_format.get("user_id"), place_args["user_id"])
        storage.delete(place)

    def test_view_singe_place_error(self):
        '''This is the 'test_view_single_place_error' method.

        Tests the 'view_single_place' method with id error.
        '''
        place_args = {"name": "test", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "TT"}
        place = Place(**place_args)
        place.save()

        rv = self.app.get('{}/places/{}/'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(place)

    def test_delete_place(self):
        '''This is the 'test_delete_place' method.

        Tests the 'delete_place' method.
        '''
        place_args = {"name": "test", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "TT"}
        place = Place(**place_args)
        place.save()

        rv = self.app.delete('{}/places/{}/'.format(
            self.path, place_args["id"]), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format, {})
        self.assertIsNone(storage.get("Place", place_args["id"]))

    def test_delete_place_error(self):
        '''This is the 'test_delete_place_error' method.

        Tests the 'delete_place' method with non-matching id.
        '''
        place_args = {"name": "cage", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "CA"}
        place = Place(**place_args)
        place.save()

        rv = self.app.delete('{}/places/{}/'.format(self.path, "noID"),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(place)

    def test_create_place(self):
        '''This is the 'test_create_place' method.

        Tests the 'create_place' method.
        '''
        place_args = {"name": "test",
                      "user_id": self.user.id, "id": "TT"}

        rv = self.app.post('{}/cities/{}/places/'.format(
            self.path, self.city.id), content_type="application/json",
                           data=json.dumps(place_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), place_args["name"])
        self.assertEqual(json_format.get("id"), place_args["id"])

        s = storage.get("Place", place_args["id"])
        self.assertIsNotNone(s)
        self.assertEqual(s.user_id, place_args["user_id"])
        storage.delete(s)

    def test_create_place_json_error(self):
        '''This is the 'test_create_place_json_error' method.

        Tests the 'create_place' method with invalid JSON.
        '''
        place_args = {"name": "test",
                      "user_id": self.user.id, "id": "TT"}

        rv = self.app.post('{}/cities/{}/places/'.format(
            self.path, self.city.id), content_type="application/json",
                           data=place_args,
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")

    def test_create_place_name_error(self):
        '''This is the 'test_create_place_name_error' method.

        Tests the 'create_place' method with misssing name value.
        '''
        place_args = {"user_id": self.user.id, "id": "TT"}

        rv = self.app.post('{}/cities/{}/places/'.format(
            self.path, self.city.id), content_type="application/json",
                           data=json.dumps(place_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Missing name")

    def test_create_place_uid_error(self):
        '''This is the 'test_create_place_uid_error' method.

        Tests the 'create_place' method with missing user_id.
        '''
        place_args = {"name": "test", "id": "TT"}

        rv = self.app.post('{}/cities/{}/places/'.format(
            self.path, self.city.id), content_type="application/json",
                           data=json.dumps(place_args), follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Missing user_id")

    def test_create_place_uid_invalid(self):
        '''This is the 'test_create_place_uid_invalid' method.

        Tests the 'create_place' method with invalid user_id.
        '''
        place_args = {"name": "test", "user_id": "noID", "id": "TT"}

        rv = self.app.post('{}/cities/{}/places/'.format(
            self.path, self.city.id), content_type="application/json",
                           data=json.dumps(place_args), follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_create_place_cid_error(self):
        '''This is the 'test_create_place_cid_error' method.

        Tests the 'create_place' method with invalid city_id.
        '''
        place_args = {"name": "test", "user_id": "noID", "id": "TT"}

        rv = self.app.post('{}/cities/{}/places/'.format(self.path, "noID"),
                           content_type="application/json",
                           data=json.dumps(place_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 404)

    def test_update_place_name(self):
        '''This is the 'test_update_place_name' method.

        Tests for updating name via the 'update_place' method.
        '''
        place_args = {"name": "test", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "TT"}
        place = Place(**place_args)
        place.save()

        rv = self.app.put('{}/places/{}/'.format(self.path, place.id),
                          content_type="application/json",
                          data=json.dumps({"name": "T"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), "T")
        self.assertEqual(json_format.get("id"), place_args["id"])
        self.assertEqual(json_format.get("user_id"), place_args["user_id"])
        self.assertEqual(json_format.get("city_id"), place_args["city_id"])
        storage.delete(place)

    def test_update_place_id(self):
        '''This is the 'test_update_place_id' method.

        Tests for updating id via the 'update_place' method.
        '''
        place_args = {"name": "test", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "TT"}
        place = Place(**place_args)
        place.save()

        rv = self.app.put('{}/places/{}/'.format(self.path, place.id),
                          content_type="application/json",
                          data=json.dumps({"id": "T"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), place_args["name"])
        self.assertEqual(json_format.get("id"), place_args["id"])
        self.assertEqual(json_format.get("city_id"), place_args["city_id"])
        self.assertEqual(json_format.get("user_id"), place_args["user_id"])
        storage.delete(place)

    def test_update_place_cid(self):
        '''This is the 'test_update_place_cid' method.

        Tests for updating the city_id value via the 'update_place' method.
        '''
        place_args = {"name": "test", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "TT"}
        place = Place(**place_args)
        place.save()

        rv = self.app.put('{}/places/{}/'.format(self.path, place.id),
                          content_type="application/json",
                          data=json.dumps({"city_id": "T"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), place_args["name"])
        self.assertEqual(json_format.get("id"), place_args["id"])
        self.assertEqual(json_format.get("city_id"), place_args["city_id"])
        self.assertEqual(json_format.get("user_id"), place_args["user_id"])
        storage.delete(place)

    def test_update_place_uid(self):
        '''This is the 'test_update_place_uid' method.

        Tests for updating the user_id value via the 'update_place' method.
        '''
        place_args = {"name": "test", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "TT"}
        place = Place(**place_args)
        place.save()

        rv = self.app.put('{}/places/{}/'.format(self.path, place.id),
                          content_type="application/json",
                          data=json.dumps({"user_id": "T"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), place_args["name"])
        self.assertEqual(json_format.get("id"), place_args["id"])
        self.assertEqual(json_format.get("city_id"), place_args["city_id"])
        self.assertEqual(json_format.get("user_id"), place_args["user_id"])
        storage.delete(place)

    def test_update_place_json_error(self):
        '''This is the 'test_update_place_json_error' method.

        Tests the 'update_place' method with invalid JSON.
        '''
        place_args = {"name": "test", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "TT"}
        place = Place(**place_args)
        place.save()

        rv = self.app.put('{}/places/{}/'.format(self.path, place.id),
                          content_type="application/json",
                          data={"id": "T"},
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")
        storage.delete(place)

    def test_update_place_cid_error(self):
        '''This is the 'test_update_place_cid_error' method.

        Tests the 'update_place' method with invalid cid.
        '''
        place_args = {"name": "test", "city_id": self.city.id,
                      "user_id": self.user.id, "id": "TT"}
        place = Place(**place_args)
        place.save()

        rv = self.app.put('{}/places/{}/'.format(self.path, "noID"),
                          content_type="application/json",
                          data=json.dumps({"name": "T"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(place)


if __name__ == "__main__":
    unittest.main()
