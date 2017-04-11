#!/usr/bin/python3
'''

This is the 'test_users' module.

test_users is the testing suite for the 'users' module.


'''
from api.v1.app import (app)
import flask
import json
from models import storage
from models.user import User
import unittest


def get_json(response):
    '''This is the 'get_json' method.

    Requests a JSON object from a flask response object.
    '''
    return json.loads(str(response.get_data(), encoding="utf-8"))


class TestUserView(unittest.TestCase):
    '''This is the 'TestUserView' class.

    This is the test suite for the 'users' module.
    '''

    @classmethod
    def setUpClass(cls):
        '''This is the 'setUpClass' method.

        Set up for testing suite.
        '''
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.path = "/api/v1"

    def test_view_user(self):
        '''This is the 'test_view_user' method.

        Tests the 'view_user' method.
        '''
        user_args = {"first_name": "test", "email": "test@test.com",
                     "password": "test"}
        user = User(**user_args)
        user.save()

        rv = self.app.get('{}/users/'.format(self.path),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertTrue(type(json_format), list)
        self.assertIn(user_args["first_name"], [e.get(
            "first_name") for e in json_format])
        self.assertIn(user_args["email"], [e.get(
            "email") for e in json_format])
        storage.delete(user)

    def test_view_single_user(self):
        '''This is the 'test_view_single_user' method.

        Tests for accessing a single User object using the 'view_user' method.
        '''
        user_args = {"first_name": "test", "id": "TS2",
                     "email": "test@test.com", "password": "test"}
        user = User(**user_args)
        user.save()

        rv = self.app.get('{}/users/{}'.format(
            self.path, user_args["id"]), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get(
            "first_name"), user_args["first_name"])
        self.assertEqual(json_format.get("id"), user_args["id"])
        self.assertEqual(json_format.get("email"), user_args["email"])
        storage.delete(user)

    def test_view_single_user_wrong(self):
        '''This is the 'test_view_single_user_error' method.

        Tests for accessing a single User object, passing an invalid name.
        '''
        user_args = {"first_name": "test", "id": "TS1",
                     "email": "test@test.com", "password": "test"}
        user = User(**user_args)
        user.save()

        rv = self.app.get('{}/users/{}'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(user)

    def test_delete_user(self):
        '''This is the 'test_delete_user' method.

        Tests for deleting a User object.
        '''
        user_args = {"first_name": "test", "id": "TS",
                     "email": "test@test.com", "password": "test"}
        user = User(**user_args)
        user.save()

        rv = self.app.delete('{}/users/{}/'.format(
            self.path, user_args["id"]),
                                   follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format, {})
        self.assertIsNone(storage.get("User", user_args["id"]))

    def test_delete_user_error(self):
        '''This is the 'test_delete_user_error' method.

        Tests for deleting a User object.
        '''
        user_args = {"first_name": "test", "id": "TS",
                     "email": "test@test.com", "password": "test"}
        user = User(**user_args)
        user.save()

        rv = self.app.delete('{}/users/{}/'.format(self.path, "noID"),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(user)

    def test_create_user(self):
        '''This is the 'test_create_user' method.

        Tests for the 'create_user' method.
        '''
        user_args = {"first_name": "test", "id": "TS",
                     "email": "test@test.com", "password": "test"}

        rv = self.app.post('{}/users/'.format(self.path),
                           content_type="application/json",
                           data=json.dumps(user_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get(
            "first_name"), user_args["first_name"])
        self.assertEqual(json_format.get("id"), user_args["id"])
        self.assertEqual(json_format.get("email"), user_args["email"])

        s = storage.get("User", user_args["id"])
        self.assertIsNotNone(s)
        storage.delete(s)

    def test_create_user_json_error(self):
        '''This is the 'test_create_user_json_error' method.

        Tests for creation of User object with invalid JSON.
        '''
        user_args = {"first_name": "test", "id": "TS",
                     "email": "test@test.com", "password": "test"}

        rv = self.app.post('{}/users/'.format(self.path),
                           content_type="application/json",
                           data=user_args,
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")

    def test_create_user_email_error(self):
        '''This is the 'test_create_user_email_error' method.

        Tests for creation of User object with no email.
        '''
        user_args = {"id": "TS2",
                     "password": "test"}

        rv = self.app.post('{}/users/'.format(self.path),
                           content_type="application/json",
                           data=json.dumps(user_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Missing email")

    def test_create_user_pwd_error(self):
        '''This is the 'test_create_user_pwd_error' method.

        Tests for creation of User object with no password.
        '''
        user_args = {"id": "TS2",
                     "email": "test"}

        rv = self.app.post('{}/users/'.format(self.path),
                           content_type="application/json",
                           data=json.dumps(user_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Missing password")

    def test_update_user_first_name(self):
        '''This is the 'test_update_user_name' method.

        Tests for updating user name using the 'update_user' method.
        '''
        user_args = {"first_name": "testName", "id": "TN1",
                     "email": "testName@test.com", "password": "test"}
        user = User(**user_args)
        user.save()

        rv = self.app.put('{}/users/{}/'.format(self.path, user.id),
                          content_type="application/json",
                          data=json.dumps({"first_name": "T"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("first_name"), "T")
        self.assertEqual(json_format.get("id"), user_args["id"])
        self.assertEqual(json_format.get("email"), user_args["email"])
        storage.delete(user)

    def test_update_user_id(self):
        '''This is the 'test_update_user_id' method.

        Tests for updating user_id via the 'update_user' method.
        '''
        user_args = {"first_name": "test", "id": "TS1",
                     "email": "test@test.com", "password": "test"}
        user = User(**user_args)
        user.save()

        rv = self.app.put('{}/users/{}/'.format(self.path, user.id),
                          content_type="application/json",
                          data=json.dumps({"id": "T"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("first_name"),
                         user_args["first_name"])
        self.assertEqual(json_format.get("id"), user_args["id"])
        self.assertEqual(json_format.get("email"), user_args["email"])
        storage.delete(user)

    def test_update_user_email(self):
        '''This is the 'test_update_user_email' method

        Tests for updating user email value.
        '''
        user_args = {"first_name": "test", "id": "TS1",
                     "email": "test@test.com", "password": "test"}
        user = User(**user_args)
        user.save()
        rv = self.app.put('{}/users/{}/'.format(self.path, user.id),
                          content_type="application/json",
                          data=json.dumps({"email": "T@t.com"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("first_name"),
                         user_args["first_name"])
        self.assertEqual(json_format.get("id"), user_args["id"])
        self.assertEqual(json_format.get("email"), user_args["email"])
        storage.delete(user)

    def test_update_user_json_error(self):
        '''This is the 'test_update_user_json_error' method.

        Tests the 'update_user' method with invalid JSON.
        '''
        user_args = {"first_name": "test", "id": "TS2",
                     "email": "test@test.com", "password": "test"}
        user = User(**user_args)
        user.save()

        rv = self.app.put('{}/users/{}/'.format(self.path, user.id),
                          content_type="application/json",
                          data={"id": "T"},
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")
        storage.delete(user)

    def test_update_user_id_error(self):
        '''This is the 'test_update_user_id_error' method.

        Tests the 'update_user' method with an invalid user_id.
        '''
        user_args = {"first_name": "test", "id": "TS",
                     "email": "test@test.com", "password": "test"}
        user = User(**user_args)
        user.save()

        rv = self.app.put('{}/users/{}/'.format(self.path, "noID"),
                          content_type="application/json",
                          data=json.dumps({"id": "T"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(user)


if __name__ == "__main__":
    unittest.main()
