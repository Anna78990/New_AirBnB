#!/usr/bin/python3
""" Starts a Flash Web Application """
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
import bcrypt


app = Flask(__name__)

type_s = getenv('HBNB_TYPE_STORAGE')

if type_s == "db":
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        link_db = ('mysql+pymysql://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        app.config['SQLALCHEMY_DATABASE_URI'] = link_db  # SQLiteデータベースのURI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True
app.secret_key = os.urandom(24)

@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/101-hbnb', strict_slashes=False)
def hbnb():
    """ HBNB is alive! """
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    st_ct = []

    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    return render_template('101-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places,
                           cache_id=uuid4())


@app.route('/places/<place_id>', strict_slashes=False)
def place_detail(place_id):
    """ Place detail page """
    place = storage.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")
    return render_template('place_detail.html', place=place, cache_id=uuid4())


@app.route('/user_registration', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        if not validate_email(email):
            return render_template('register.html', error='Invalid email format')
        if not validate_password(password):
            return render_template('register.html', error='Password must be at least 6 characters long')

        password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(email=email, password=password_hashed, first_name=first_name, last_name=last_name)
        storage.new(new_user)
        storage.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.before_request
def store_last_visited_url():
    if request.endpoint not in ['login', 'static']:
        session['last_visited_url'] = request.url


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = storage.get_by_attribute(User, email=email)
        # print(f'pass input: {password}, pass db: {user.password}')

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['user_id'] = user.id
            return redirect(url_for('hbnb'))
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_password(password):
    return len(password) >= 6

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in data:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in data:
        return jsonify({'error': 'Missing password'}), 400

    email = data['email']
    password = data['password']
    first_name = data.get('first_name', "")
    last_name = data.get('last_name', "")

    if not validate_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    if not validate_password(password):
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400

    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(email=email, password=password_hashed, first_name=first_name, last_name=last_name)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201

@app.route('/check_login_status')
def check_login_status():
    if 'user_id' in session:
        return jsonify({'logged_in': True})
    else:
        return jsonify({'logged_in': False})


if __name__ == "__main__":
    """ Main Function """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain('cert.pem', 'key.pem')
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    app.run(host='127.0.0.1', port=5000, ssl_context=context, debug=True)
