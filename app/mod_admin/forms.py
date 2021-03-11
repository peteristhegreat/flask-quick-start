# app/mod_admin/forms.py
# TODO: make forms for each table in firebase

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import validators
# from app.wtforms.utils import BootstrapVerifyEmail, BootstrapVerifyPassword, BootstrapVerifyText
from wtforms.validators import Email, EqualTo

from wtforms_widgets.base_form import BaseForm
from wtforms_widgets.fields.core import StringField, PasswordField, BooleanField, IntegerField, \
    DateTimeField, SelectField
from wtforms_widgets.fields.custom import ReadonlyTextField

from app import firebase


class UserForm(BaseForm):
    id = IntegerField("User Id", [validators.DataRequired(message='Must provide a user id')])
    # last_login_dt = DateTimeField("Last Login Date") # datepicker_options
    # created_dt = DateTimeField("Created Date")
    identity_hash = ReadonlyTextField('ID Hash')
    role = SelectField("Role", choices=[('admin', 'Admin'), ('receiver', 'Receiver'), ('sender', 'Sender'),
                                        ('pending', "Pending"), ("denylist", "Denied")])
    registration_attempts = IntegerField("Registration Attempts")
    comment = StringField("Comment")
    locale = SelectField("Language", choices=[("en", "English"), ("es", "Spanish")])
    deleted = BooleanField("Deleted (flag)")