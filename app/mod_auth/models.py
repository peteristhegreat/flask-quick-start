from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# from app import db
# from flask import session


# https://stackoverflow.com/questions/63231163/what-is-usermixin-in-flask
class User(UserMixin):
    # def __init__(self, session):
    #     # self.id = session["profile"]["user"]["localId"]
    #     # self.email = session["profile"]["user"]["email"]
    #     # self.verified = session["profile"]["account_info"]["emailVerified"]

    def __init__(self, id_token, account_info):
        self.id = account_info["users"][0]["localId"]
        self.email = account_info["users"][0]["email"]
        self.idToken = id_token
        self.verified = account_info["users"][0]["emailVerified"]

    def get_id(self):
        return self.idToken

    def is_authenticated(self):
        return self.id is not None and self.verified

    def is_active(self):
        # TODO: check session["profile"]["account_info"]["lastRefreshAt"] to see if it is active
        return True

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User{}>'.format(self.email)