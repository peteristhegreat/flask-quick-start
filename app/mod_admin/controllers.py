# app/mod_admin/controllers.py
# TODO: make routes and blueprint for mod_admin for handling forms and editing elements in firebase

from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

mod_admin = Blueprint('admin', __name__, url_prefix='/admin')


@mod_admin.route('/', methods=['GET', 'POST'])
def admin_index():
    return render_template("admin/index.html")