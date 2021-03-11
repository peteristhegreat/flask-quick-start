from flask_wtf import FlaskForm, RecaptchaField
from wtforms import validators
# from app.wtforms.utils import BootstrapVerifyEmail, BootstrapVerifyPassword, BootstrapVerifyText
from wtforms.validators import Email, EqualTo

from wtforms_widgets.base_form import BaseForm
from wtforms_widgets.fields.core import StringField, PasswordField, BooleanField

from app import firebase


# Import Form validators


class LoginForm(BaseForm):
    email = StringField('Email Address', [Email(), validators.DataRequired(message='Forgot your email address?')])
    password = PasswordField('Password', [validators.DataRequired(message='Must provide a password. ;-)')])
    remember_me = BooleanField()


class RegisterForm(BaseForm):
    name = StringField('Username', [validators.DataRequired(), validators.Length(max=255)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8)])
    email = StringField('Email Address', [Email(), validators.DataRequired(), validators.Length(min=6, max=35)])
    # recaptcha = RecaptchaField()

    # auth.send_email_verification(user['idToken'])
    # auth.create_user_with_email_and_password(email, password)


class EmailOnlyForm(BaseForm):
    email = StringField('Email Address', [Email(), validators.DataRequired(), validators.Length(min=6, max=35)])
