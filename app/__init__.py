# Import flask and template operators
from flask import Flask, render_template, url_for, jsonify

# Import SQLAlchemy
# from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)
# static_url_path='static'
# static_folder='static'
# template_folder='templates'

# Configurations
app.config.from_object('config')


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

from app.jinja.jinja_asset import AssetExtension

app.jinja_env.add_extension('app.jinja.jinja_asset.AssetExtension')

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(admin_module)
app.register_blueprint(todo_list_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
# db.create_all()
