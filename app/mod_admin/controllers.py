# app/mod_admin/controllers.py
# TODO: make routes and blueprint for mod_admin for handling forms and editing elements in firebase

from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for

from app.mod_admin.forms import UserForm

import os
from .. import app
from app import db, auth


# db = firestore.client() # OLD WAY
# db = firebase.database()
# user_ref = db.collection('users') # OLD WAY
user_ref = db.child("users")

mod_admin = Blueprint('admin', __name__, url_prefix='/admin')


@mod_admin.route('/', methods=['GET', 'POST'])
def admin_index():
    return render_template("admin/index.html")


@mod_admin.route('/users', methods=['GET', 'POST'])
def admin_users():
    form = UserForm(request.form)
    if form.validate_on_submit():
        print(form)
        my_id = form.id.data
        # TODO: get the rest of the fields from the UserForm to put in the db

        data = {}
        for field in form:
            data[field.name] = field.data

        user_ref.child(data["id"]).set(data)
        flash("user item received!", 'error-message')
        # flash('Wrong email or password', 'error-message')

    # users = [doc.to_dict() for doc in user_ref.stream()] # OLD WAY

    resp = user_ref.get()
    #users = [doc.to_dict() for doc in user_ref.get()]
    #print(users)

    return render_template('admin/users.html', users=[], form=form)
    # return render_template("admin/users.html")


@mod_admin.route('/transactions', methods=['GET', 'POST'])
def admin_transactions():
    return render_template("admin/transactions.html")


@mod_admin.route('/requests', methods=['GET', 'POST'])
def admin_requests():
    return render_template("admin/requests.html")
