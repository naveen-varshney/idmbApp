import time
import json
import unittest
from flask_testing import TestCase
from imdbapp.api.models import User, UserToken
from imdbapp import create_app


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app = create_app()
        app.config["Testing"] = True
        return app


def register_user(self, name, email, password):
    return self.client.post(
        "/api/v1/users/register",
        data=json.dumps(dict(name=name, email=email, password=password)),
        content_type="application/json",
    )


def login_user(self, email, password):
    return self.client.post(
        "/api/v1/users/login",
        data=json.dumps(dict(email=email, password=password)),
        content_type="application/json",
    )


class TestAuthBlueprint(BaseTestCase):
    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = register_user(self, "Naveen", "joe8@gmail.com", "123456")
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "success")
            self.assertTrue(data["message"] == "Successfully registered.")
            self.assertTrue(data["auth_token"])
            self.assertTrue(response.content_type == "application/json")
            self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        user = User(email="joe@gmail.com", password="test")
        with self.client:
            response = register_user(self, "Naveen", "joe@gmail.com", "123456")
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "fail")
            self.assertTrue(data["message"] == "User already exists. Please Log in.")
            self.assertTrue(response.content_type == "application/json")
            self.assertEqual(response.status_code, 202)

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            resp_register = login_user(self, "joe@gmail.com", "123456")

            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register["status"] == "success")
            self.assertTrue(data_register["message"] == "Successfully logged in.")
            self.assertTrue(data_register["auth_token"])
            self.assertTrue(resp_register.content_type == "application/json")
            self.assertEqual(resp_register.status_code, 200)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = login_user(self, "joe1@gmail.com", "123456")
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "fail")
            self.assertTrue(data["message"] == "User does not exist.")
            self.assertTrue(response.content_type == "application/json")
            self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
