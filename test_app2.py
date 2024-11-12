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

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # テストクライアントの設定
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_invalid_email_format(self):
        # 不正なEメール形式のテスト
        response = self.app.post('/user_registration', data={
            'email': 'invalid-email',
            'password': 'ValidPass123',
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertIn(b'Invalid email format', response.data)

    def test_duplicate_email(self):
        # 既に登録済みのEメールのテスト
        storage.new(User(email='test@example.com', password='ValidPass123', first_name='Test', last_name='User'))
        storage.save()

        response = self.app.post('/user_registration', data={
            'email': 'test@example.com',
            'password': 'ValidPass123',
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertIn(b'Email is already registered', response.data)

    def test_invalid_password_too_short(self):
        # パスワードが短すぎるテスト
        response = self.app.post('/user_registration', data={
            'email': 'valid@example.com',
            'password': 'short',
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertIn(b'Password must be at least 6 characters long', response.data)

    def test_invalid_password_too_long(self):
        # パスワードが長すぎるテスト
        response = self.app.post('/user_registration', data={
            'email': 'valid@example.com',
            'password': 'a' * 19,  # 19文字のパスワード
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertIn(b'Password must be at least 6 characters long', response.data)

if __name__ == '__main__':
    unittest.main()

