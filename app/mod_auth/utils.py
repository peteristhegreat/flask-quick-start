from flask import session, redirect, request
from functools import wraps

key_proof_of_logged_in = "auth_id"


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        session["redirect_after_login"] = request.url
        if key_proof_of_logged_in not in session:
            return redirect('/logout')
        return f(*args, **kwargs)

    return decorated
