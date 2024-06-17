# test_app.py
import unittest
from flask import session, json
from api import v1
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User
from os import environ, getenv
from flask import Flask, render_template, abort, request, jsonify, session, redirect, url_for
from uuid import uuid4
import ssl
from hashlib import md5
import re
import os
from web_dynamic.hbnb import app 
import bcrypt
import web_dynamic

class HbnbTestCase(unittest.TestCase):
    def setUp(self):
        """Setup the Flask test client and other test requirements."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Remove the app context."""
        self.app_context.pop()

    def test_hbnb_route(self):
        """Test the /101-hbnb route."""
        response = self.client.get('/101-hbnb')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'HBnB', response.data)

    def test_place_detail_route(self):
        """Test the /places/<place_id> route."""
        place = next(iter(storage.all('Place').values()))
        if place:
            response = self.client.get(f'/places/{place.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(place.name.encode(), response.data)
        else:
            self.skipTest('No places found in the database.')

    def test_user_registration(self):
        """Test user registration."""
        response = self.client.post('/user_registration', data={
            'email': 'testuser@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/login')

    def test_login(self):
        """Test user login."""
        # Create a test user
        email = 'testuser@example.com'
        password = 'password123'
        password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(email=email, password=password_hashed, first_name='Test', last_name='User')
        storage.new(new_user)
        storage.save()

        # Test login
        response = self.client.post('/login', data={
            'email': email,
            'password': password
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/101-hbnb')

    def test_create_user_api(self):
        """Test the /api/v1/users route."""
        response = self.client.post('/api/v1/users', json={
            'email': 'apiuser@example.com',
            'password': 'password123',
            'first_name': 'API',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['email'], 'apiuser@example.com')

    def test_check_login_status(self):
        """Test the /check_login_status route."""
        with self.client:
            response = self.client.get('/check_login_status')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertFalse(data['logged_in'])

            self.client.post('/login', data={
                'email': 'testuser@example.com',
                'password': 'password123'
            })
            response = self.client.get('/check_login_status')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['logged_in'])


if __name__ == '__main__':
    unittest.main()
