import os
from functools import wraps
from flask import session, redirect, url_for


def is_login_required():
    return os.environ.get('LOGIN_REQUIRED', 'true').lower() in ('true', '1', 't')


def login_is_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_login_required():
            return f(*args, **kwargs)
        if "google_id" not in session:
            return redirect(url_for('login'))
        else:
            return f(*args, **kwargs)

    return wrapper


def already_logged_in(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_login_required():
            return redirect(url_for('dashboard'))
        if "google_id" in session:
            return redirect(url_for('dashboard'))
        else:
            return f(*args, **kwargs)

    return wrapper
