#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.reservation import Reservation
from models.user import User
from os import environ, getenv
from flask import Flask, render_template, abort, request, jsonify, session, redirect, url_for
from flask_babel import Babel, gettext as _
from uuid import uuid4
import ssl
from hashlib import md5
import re
import os
import bcrypt
from datetime import datetime


app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'fr']

app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'


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

def get_locale():
    best_match = request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])
    print(f"Locale selected: {best_match}")  # デバッグ用の出力
    return best_match
    #return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])

babel = Babel(app, locale_selector=get_locale)

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

        is_valid, message = validate_email(email, storage)
        if not is_valid:
            return render_template('register.html', error=message)
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

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password
                                   if isinstance(user.password, bytes) else user.password.encode('utf-8')):
            session['user_id'] = user.id
            return redirect(url_for('hbnb'))
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')

def validate_email(email, storage):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_regex, email) is None:
        return False, "Invalid email format"

    existing_user = storage.get_by_attribute(User, email=email)
    if existing_user is not None:
        return False, "Email is already registered"

    return True, "Email is valid"

def validate_password(password):
    return 6 <= len(password) <= 18

@app.route('/book_now/<place_id>', methods=['GET', 'POST'])
def book_now(place_id):
    """Book now page"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")
    
    if request.method == 'POST':
        if 'user_id' not in session:
            return redirect(url_for('login'))

        user_id = session['user_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return render_template('book_now.html', place=place, error='Invalid date format')

        new_reservation = Reservation(user_id=user_id, place_id=place_id, start_date=start_date, end_date=end_date)
        storage.new(new_reservation)
        storage.save()

        return redirect(url_for('thankyou'))

    return render_template('book_now.html', place=place)

@app.route('/user/<user_id>', strict_slashes=False)
def user_page(user_id):
    """User page showing all reservations"""
    user = storage.get(User, user_id)
    if not user:
        abort(404, description="User not found")
    
    reservations = user.reservations
    return render_template('user_page.html', user=user, reservations=reservations, cache_id=uuid4())


@app.route('/check_login_status')
def check_login_status():
    if 'user_id' in session:
        user_id = session['user_id']
        return jsonify({'logged_in': True, 'user_id': user_id})
    else:
        return jsonify({'logged_in': False})

@app.route('/reservation_completed')
def thankyou():
    return render_template('reserve_completed.html')

if __name__ == "__main__":
    """ Main Function """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain('cert.pem', 'key.pem')
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    app.run(host='127.0.0.1', port=5000, ssl_context=context, debug=True)
    app.run(host='127.0.0.1', port=5000)
