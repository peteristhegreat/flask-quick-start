from flask_wtf import FlaskForm, RecaptchaField
from wtforms import PasswordField, TextAreaField, StringField, validators

# Import Form validators
from wtforms.validators import Email, EqualTo


class ToDoForm(FlaskForm):
    id = StringField('Id', [validators.DataRequired(message='Forgot the id?')])
    description = StringField('Description', [
        validators.DataRequired(message='Describe your todo')])
