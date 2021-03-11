# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for

import flask_login
from flask_login import login_required

# Import module forms
from app.mod_auth.forms import LoginForm, RegisterForm, EmailOnlyForm
from app.mod_auth.models import User

from app import auth
from requests.exceptions import HTTPError
import json

from ppretty import ppretty

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    # Forgot/Sent password link to email
    form = EmailOnlyForm(request.form)
    sent = False
    email = ""
    if form.validate_on_submit():
        email = form.email.data
        try:
            resp = auth.send_password_reset_email(email)
        except HTTPError as e:
            error_dict = json.loads(e.strerror)
            print("Email %s is %s because %s" % (email, error_dict["error"]["message"], error_dict["error"]["errors"][0]["reason"]))
        sent = True

    return render_template("auth/forgot.html", form=form, sent=sent, email=email)


@mod_auth.route('/', methods=['GET'])
@login_required
def home():
    user_id = flask_login.current_user.id
    verified = session["profile"]["account_info"]["emailVerified"]
    return render_template("auth/home.html", verified=verified, user_id=user_id)


@mod_auth.route('/verify_email', methods=['GET'])
@login_required
def send_verify_email():
    email = session["profile"]["user"]["email"]
    try:
        auth.send_email_verification(session["profile"]["user"]['idToken'])
    except HTTPError as e:
        error_dict = json.loads(e.strerror)
        print("Email %s is %s because %s" % (email, error_dict["error"]["message"], error_dict["error"]["errors"][0]["reason"]))
        if error_dict["error"]["message"] == "TOO_MANY_ATTEMPTS_TRY_LATER":
            flash("Too many attempts to verify email. Try again later.")
        return redirect(url_for("auth.home"))

    return render_template("auth/verify_email.html", sent=True, email=email)


# Set the route and accepted methods
@mod_auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    flask_login.logout_user()
    session["profile"] = {}
    flash("Logged out.")
    return redirect(url_for("auth.login_existing_user"))


# Set the route and accepted methods
@mod_auth.route('/login', methods=['GET', 'POST'])
def login_existing_user():
    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():
        # print(form.email.data)
        # print(form.password.data)
        email = form.email.data
        try:
            user = auth.sign_in_with_email_and_password(form.email.data, form.password.data)
        except HTTPError as e:
            error_dict = json.loads(e.strerror)
            print("Login failed, email %s is %s because %s" % (email, error_dict["error"]["message"], error_dict["error"]["errors"][0]["reason"]))
            flash('Wrong email or password', 'error-message')
            return render_template("auth/login.html", form=form)

        for key in ["kind", "localId", "email", "displayName", "registered", "expiresIn"]:
            print("user['%s'] = %s" % (key, user[key]))
        for key in ["idToken", "refreshToken"]:
            print("user['%s'] = %s****%s (len = %d)" % (key, user[key][0:4], user[key][-4:], len(user[key])))

        # user['kind'] = identitytoolkit# VerifyPasswordResponse
        # user['localId'] = rjXlH8WdmNO4rxcXRaoa12pInq42
        # user['email'] = peteristhegreat@hotmail.com
        # user['displayName'] =
        # user['registered'] = True
        # user['expiresIn'] = 3600
        # user['idToken'] = eyJh ** ** I8RQ(len=937)
        # user['refreshToken'] = AOvu ** ** uOow(len=226)

        info = auth.get_account_info(user['idToken'])
        if False:
            print("info", ppretty(info, seq_length=20, depth=6, indent="  "))
        # {
        #     'kind': 'identitytoolkit#GetAccountInfoResponse',
        #     'users': [
        #         {
        #             'localId': 'rjXlH*****',
        #             'email': 'email@example.com',
        #             'passwordHash': 'UkVE***',
        #             'emailVerified': False,
        #             'passwordUpdatedAt': 1615462413755,
        #             'providerUserInfo': [
        #                 {
        #                     'providerId': 'password',
        #                     'federatedId': 'email@example.com',
        #                     'email': 'email@example.com',
        #                     'rawId': 'email@example.com'
        #                 }
        #             ],
        #             'validSince': '1615462413',
        #             'lastLoginAt': '1615471593505',
        #             'createdAt': '1615462413755',
        #             'lastRefreshAt': '2021-03-11T14:06:33.505Z'
        #         }
        #     ]
        # }

        flask_login.login_user(User(user["idToken"], info))
        session["profile"] = {}
        session["profile"]["verified"] = info["users"][0]["emailVerified"]
        session["profile"]["account_info"] = info["users"][0]
        session["profile"]["user"] = user
            # render_template("auth/verify_email.html", sent=False, email=email)
        # user

        # session["idToken"] = user['idToken']
        # session["profile"] = {
        #     'user_id': userinfo['sub'],
        #     'name': userinfo['name'],
        #     'picture': userinfo['picture']
        # }
        return redirect(url_for("auth.home"))

    return render_template("auth/login.html", form=form)


@mod_auth.route('/register', methods=['GET', 'POST'])
def register_new_user():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # TODO: validate the registration from the db
        print("form received and validated!")
        # print(form)
        print(form.name, form.name.data)
        print(form.email, form.email.data)
        print(form.password, form.password.data)
        user = auth.create_user_with_email_and_password(form.email.data, form.password.data)
        email = form.email.data

        auth.send_email_verification(user['idToken'])
        render_template("auth/verify_email.html", sent=True, email=email)

    return render_template("auth/register.html", form=form)
