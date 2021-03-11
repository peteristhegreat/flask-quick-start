# Import flask and template operators
from flask import Flask, render_template, url_for, jsonify, session

import pyrebase
import os
import json
from ppretty import ppretty
from flask_login import LoginManager
from app.mod_auth.models import User
from flask_babel import gettext, Babel
from requests.exceptions import HTTPError

# Import SQLAlchemypip
# from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)
# static_url_path='static'
# static_folder='static'
# template_folder='templates'

# Configurations
app.config.from_object('config')
babel = Babel(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

firebase_key_json = os.path.join(app.config['BASE_DIR'], 'key.json')
pyrebase_key_json = os.path.join(app.config['BASE_DIR'], 'pyrebase-key.json')
with open("pyrebase-key.json", "r") as jfile:
    firebase_config = json.loads(jfile.read())
firebase_config["serviceAccount"] = firebase_key_json

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()


# OLD WAY of using firebase_admin for everything, now use firebase.auth instead
# from firebase_admin import credentials, firestore, initialize_app
#
# firebase_key_json = os.path.join(app.config['BASE_DIR'], 'key.json')
# cred = credentials.Certificate(firebase_key_json)
# firebase = initialize_app(cred)

# Define the database object which is imported
# by modules and controllers
# db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(400)
def not_found(error):
    return render_template('error/400.html'), 400


@app.errorhandler(401)
def not_found(error):
    return render_template('error/401.html'), 401


@app.errorhandler(403)
def not_found(error):
    return render_template('error/403.html'), 403


@app.errorhandler(404)
def not_found(error):
    return render_template('error/404.html'), 404


# https://flask-login.readthedocs.io/en/latest/#how-it-works
@login_manager.user_loader
def user_loader(id_token):
    try:
        # rough equivalent of looking up the user in the users table of the db
        info = auth.get_account_info(id_token)
        user = User(id_token, info)
        return user
    except HTTPError as e:
        # when the id token expires we will probably end up here
        print("user_load error", ppretty(e, seq_length=20, depth=6, indent="  "))
        return None


# https://flask-login.readthedocs.io/en/latest/#custom-login-using-request-loader
# @login_manager.request_loader
# def load_user_from_request(request):
#     # TODO: Get the user from firebase.auth instead???
#     # first, try to login using the api_key url arg
#     if session.get("profile") is None or session["profile"].get("user") is None:
#         return None
#     user = User(session)
#     return user


# @login_manager.localize_callback
# def localize_text_for_login_errors(txt):
#     if txt is not None:
#         return gettext(txt)
#     return ''


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('error/401.html')

# @babel.localeselector
# def get_locale():
#     # if a user is logged in, use the locale from the user settings
#     user = getattr(g, 'user', None)
#     if user is not None:
#         return user.locale
#     # otherwise try to guess the language from the user accept
#     # header the browser transmits.  We support de/fr/en in this
#     # example.  The best match wins.
#     return request.accept_languages.best_match(['de', 'fr', 'en'])
#
# @babel.timezoneselector
# def get_timezone():
#     user = getattr(g, 'user', None)
#     if user is not None:
#         return user.timezone

# from werkzeug.exceptions import HTTPException, InternalServerError
#
# @app.errorhandler(InternalServerError)
# def handle_500(e):
#     original = getattr(e, "original_exception", None)
#
#     if original is None:
#         # direct 500 error, such as abort(500)
#         return render_template("error/500.html"), 500
#
#     # wrapped unhandled error
#     return render_template("error/500_unhandled.html", e=original), 500


@app.route('/')
def index():
    return render_template('home.html')


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/test")
def test_page():
    return render_template("test.html")


@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    print(links)
    # return jsonify(links), 200
    return render_template("admin/site-map.html", site_map=links)


# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_admin.controllers import mod_admin as admin_module
from app.mod_todo_list.routes import mod_todo_list as todo_list_module
# from app.mod_transaction.routes import mod_transaction as transaction_module
# from app.mod_users.routes import mod_users as users_module

from app.jinja.jinja_asset import AssetExtension

app.jinja_env.add_extension('app.jinja.jinja_asset.AssetExtension')

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(admin_module)
app.register_blueprint(todo_list_module)
# app.register_blueprint(transaction_module)
# app.register_blueprint(users_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
# db.create_all()
