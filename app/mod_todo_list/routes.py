# import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for

mod_todo_list = Blueprint('todo', __name__, url_prefix='/todo')

# from flask import current_app, request, _request_ctx_stack
# from flask_jwt import JWT, jwt_required, JWTError, _jwt
#
# @jwt.request_handler
# def request_handler():
#     auth_header_value = request.headers.get('Authorization', None)
#     auth_header_prefix = current_app.config['JWT_AUTH_HEADER_PREFIX']
#     if not auth_header_value:
#         # check if flask_login is configured
#         if isinstance(current_app.login_manager, LoginManager):
#             # load user
#             current_app.login_manager._load_user()
#             # if successful, this will set user variable at request context
#             if hasattr(_request_ctx_stack.top, 'user'):
#                 # generate token
#                 access_token = _jwt.jwt_encode_callback(_request_ctx_stack.top.user)
#                 return access_token
#     parts = auth_header_value.split()
#     if parts[0].lower() != auth_header_prefix.lower():
#         raise JWTError('Invalid JWT header', 'Unsupported authorization type')
#     elif len(parts) == 1:
#         raise JWTError('Invalid JWT header', 'Token missing')
#     elif len(parts) > 2:
#         raise JWTError('Invalid JWT header', 'Token contains spaces')
#     return parts[1]

# Initialize Firestore DB
import os
from .. import app

firebase_key_json = os.path.join(app.config['BASE_DIR'], 'key.json')
cred = credentials.Certificate(firebase_key_json)
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')


@mod_todo_list.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@mod_todo_list.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents

    """
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@mod_todo_list.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@mod_todo_list.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection

    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        todo_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

from app.mod_todo_list.forms import ToDoForm

@mod_todo_list.route('/admin', methods=['GET', 'POST'])
def admin():
    form = ToDoForm(request.form)
    if form.validate_on_submit():
        print(form)
        id = form.id.data
        todo_ref.document(id).set({'id': id, 'description': form.description.data})
        flash("todo item received!", 'error-message')
        # flash('Wrong email or password', 'error-message')

    all_todos = [doc.to_dict() for doc in todo_ref.stream()]
    print(all_todos)

    return render_template('todo/crud.html', todo_items=all_todos, form=form)
