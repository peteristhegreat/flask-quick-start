from flask_wtf import FlaskForm, RecaptchaField
from wtforms import PasswordField, TextAreaField, StringField, validators

# Import Form validators
from wtforms.validators import Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email Address', [Email(),
                                          validators.DataRequired(message='Forgot your email address?')])
    password = PasswordField('Password', [
        validators.DataRequired(message='Must provide a password. ;-)')])


class RegisterForm(FlaskForm):
    name = StringField('name', [validators.DataRequired(), validators.Length(max=255)])
    password = PasswordField('new password', [validators.DataRequired(), validators.Length(min=8)])
    email = StringField('emailaddress', [validators.DataRequired(), validators.Length(min=6, max=35)])
    # recaptcha = RecaptchaField()
