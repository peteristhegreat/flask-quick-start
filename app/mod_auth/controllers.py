# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
# from app import db

# Import module forms
from app.mod_auth.forms import LoginForm, RegisterForm

# Import module models (i.e. User)
# from app.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


# Set the route and accepted methods
@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():

    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

        user = False  # User.query.filter_by(email=form.email.data).first()
        # TODO: read user list from db
        print(form.email.data)
        print(form.password.data)

        if user and check_password_hash(user.password, form.password.data):

            session['user_id'] = user.id

            flash('Welcome %s' % user.name)

            return redirect(url_for('auth.home'))

        flash('Wrong email or password', 'error-message')

    return render_template("auth/signin.html", form=form)


@mod_auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        # TODO: validate the registration from the db
        print("form received and validated!")
        # print(form)
        print(form.name, form.name.data)
        print(form.email, form.email.data)
        print(form.password, form.password.data)
        return 'the form has been submitted. Success!'

    return render_template("auth/register.html", form=form)
