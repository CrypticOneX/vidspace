from flask import session, url_for, redirect
from functools import wraps


def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'logged_in' in session and 'user_id' in session and 'channel_id' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('signin'))

    return decorated



