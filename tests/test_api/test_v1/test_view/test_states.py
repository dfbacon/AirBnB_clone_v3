#!/usr/bin/python3
'''

This is the 'test_states' module.

test_states is the testing suite for the 'states' module.

'''
from api.v1.app import (app)
import flask
import json
from models import storage
from models.state import State
import unittest


def get_json(response):
    '''This is the 'get_json' method.

    Requests a JSON object from a flask response object.
    '''
    return json.loads(str(response.get_data(), encoding="utf-8"))


class TestStatesView(unittest.TestCase):
    '''This is the 'TestStatesView' class.

    Contains tests for the 'states' module.
    '''

    @classmethod
    def setUpClass(cls):
        '''This is the 'setUpClass' method.

        Set up for testing.
        '''
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.path="/api/v1"

    def test_view_all_states(self):
        '''This is the 'test_view_all_states' method.

        Tests for the 'view_all_states' method.
        '''
        state_args = {"name": "Test"}
        state = State(**state_args)
        state.save()

        rv = self.app.get('{}/states/'.format(self.path))
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertTrue(type(json_format), list)
        self.assertIn(state_args["name"], [e.get("name") for e in json_format])
        storage.delete(state)

    def test_view_all_states_db_error(self):
        '''This is the 'test_view_all_states_db_error' method.

        Tests the 'view_all_states' method with empty database.
        '''
        rv = self.app.get('{}/states/'.format(self.path))
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertTrue(type(json_format), list)
        self.assertEqual(json_format, [])

    def test_view_single_state(self):
        '''This is the 'test_view_single_state' method.

        Tests for the 'view_single_state' method.
        '''
        state_args = {"name": "Test", "id": "TS3"}
        state = State(**state_args)
        state.save()

        rv = self.app.get('{}/states/{}'.format(self.path, state_args["id"]))
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), state_args["name"])
        self.assertEqual(json_format.get("id"), state_args["id"])
        storage.delete(state)

    def test_view_one_state_error(self):
        '''This is the 'test_view_one_state_error' method

        Tests for an incorrect id.
        '''
        state_args = {"name": "Test", "id": "TS1"}
        state = State(**state_args)
        state.save()

        rv = self.app.get('{}/states/{}'.format(self.path, "noID"))
        self.assertEqual(rv.status_code, 404)
        storage.delete(state)

    def test_delete_state(self):
        '''This is the 'test_delete_state' method.

        Tests for the 'delete_state' method.
        '''
        state_args = {"name": "Test", "id": "TS"}
        state = State(**state_args)
        state.save()

        rv = self.app.delete('{}/states/{}/'.format(
            self.path, state_args["id"]), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format, {})
        self.assertIsNone(storage.get("State", state_args["id"]))

    def test_delete_state_error(self):
        '''This is the 'test_delete_state_error' method.

        Tests for id that does not match a State object.
        '''
        state_args = {"name": "Test", "id": "TS1"}
        state = State(**state_args)
        state.save()

        rv = self.app.delete('{}/states/{}/'.format(self.path, "noID"),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(state)

    def test_create_state(self):
        '''This is the 'test_create_state' method.

        Tests for the 'create_state' method.
        '''
        state_args = {"name": "Zanzibar", "id": "ZA2"}
        rv = self.app.post('{}/states/'.format(self.path),
                           content_type="application/json",
                           data=json.dumps(state_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), state_args["name"])
        self.assertEqual(json_format.get("id"), state_args["id"])

        s = storage.get("State", state_args["id"])
        self.assertIsNotNone(s)
        storage.delete(s)

    def test_create_state_json_error(self):
        '''This is the 'test_create_state_json_error' method.

        Tests for creating state with invalid JSON.
        '''
        state_args = {"name": "Test", "id": "TS2"}
        rv = self.app.post('{}/states/'.format(self.path),
                           content_type="application/json",
                           data=state_args,
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")

    def test_create_state_name_error(self):
        '''This is the 'test_create_state_name_error' method.

        Tests for creation of a State object without a name variable.
        '''
        state_args = {"id": "TS2"}
        rv = self.app.post('{}/states/'.format(self.path),
                           content_type="application/json",
                           data=json.dumps(state_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Missing name")

    def test_update_state_name(self):
        '''This is the 'test_update_state_name' method.

        Tests for updating the name of a State object.
        '''
        state_args = {"name": "Test", "id": "TS"}
        state = State(**state_args)
        state.save()

        rv = self.app.put('{}/states/{}/'.format(self.path, state.id),
                           content_type="application/json",
                           data=json.dumps({"name": "T"}),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), "T")
        self.assertEqual(json_format.get("id"), state_args["id"])
        storage.delete(state)

    def test_update_state_id(self):
        '''This is the 'test_update_state_id' method

        Test for update of state_id
        '''
        state_args = {"name": "Test", "id": "TS4"}
        state = State(**state_args)
        state.save()

        rv = self.app.put('{}/states/{}/'.format(self.path, state.id),
                           content_type="application/json",
                           data=json.dumps({"id": "T"}),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")

        json_format = get_json(rv)
        self.assertEqual(json_format.get("name"), state_args["name"])
        self.assertEqual(json_format.get("id"), state_args["id"])
        storage.delete(state)

    def test_update_state_json_error(self):
        '''This is the 'test_update_state_json_error' method.

        Tests for update with bad JSON object.
        '''
        state_args = {"name": "Test", "id": "TS5"}
        state = State(**state_args)
        state.save()

        rv = self.app.put('{}/states/{}/'.format(self.path, state.id),
                           content_type="application/json",
                           data={"id": "T"},
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")
        storage.delete(state)

    def test_update_state_bad_id(self):
        '''This is the 'update_state_id_error' method.

        Tests for updating State object with no matching id.
        '''
        state_args = {"name": "Test", "id": "TS6"}
        state = State(**state_args)
        state.save()

        rv = self.app.put('{}/states/{}/'.format(self.path, "noID"),
                           content_type="application/json",
                           data=json.dumps({"id": "T"}),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(state)


if __name__ == "__main__":
    unittest.main()
