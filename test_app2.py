# テストファイル: tests/test_flask_app.py
import pytest
from web_dynamic.hbnb import app, bcrypt
from models import storage
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

@pytest.fixture()
def client():
    """ Flaskアプリケーションのテスト用クライアントを設定 """
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()

    # テスト前にデータベースを初期化
    with app.app_context():
        storage.reload()

    yield client

def test_hbnb_route(client):
    """ /101-hbnb のテスト """
    response = client.get('/101-hbnb')
    assert response.status_code == 200

def test_place_detail_route(client):
    """ /places/<place_id> のテスト """
    # テスト用のPlaceインスタンスを作成し、データベースに保存
    place_id = 'test_place_id'
    new_place = models.Place(id=place_id, name='Test Place')
    storage.new(new_place)
    storage.save()

    response = client.get(f'/places/{place_id}')
    assert response.status_code == 200
    assert b'Test Place' in response.data

def test_user_registration(client):
    """ ユーザー登録のテスト """
    data = {
        'email': 'test@example.com',
        'password': 'testpassword',
        'first_name': 'Test',
        'last_name': 'User'
    }
    response = client.post('/user_registration', data=data, follow_redirects=True)
    assert b'Redirecting...' in response.data

    # 登録したユーザーがデータベースに存在するか確認
    user = storage.get_by_attribute(User, email=data['email'])
    assert user is not None
    assert user.email == data['email']

def test_login(client):
    """ ログインのテスト """
    # テスト用のユーザーを作成してデータベースに保存
    password_hashed = bcrypt.hashpw('testpassword'.encode('utf-8'), bcrypt.gensalt())
    new_user = User(email='test@example.com', password=password_hashed, first_name='Test', last_name='User')
    storage.new(new_user)
    storage.save()

    data = {
        'email': 'test@example.com',
        'password': 'testpassword'
    }
    response = client.post('/login', data=data, follow_redirects=True)
    assert b'HBNB is alive!' in response.data

def test_api_create_user(client):
    """ /api/v1/users のテスト """
    data = {
        'email': 'test_api@example.com',
        'password': 'testpassword',
        'first_name': 'API',
        'last_name': 'User'
    }
    response = client.post('/api/v1/users', json=data)
    assert response.status_code == 201
    assert b'API User' in response.data

def test_check_login_status(client):
    """ /check_login_status のテスト """
    response = client.get('/check_login_status')
    assert response.status_code == 200
    assert b'logged_in' in response.data

# pytestでテストを実行するためには、コマンドラインで以下を実行します:
# pytest -v
