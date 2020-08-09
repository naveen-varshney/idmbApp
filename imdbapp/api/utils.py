from functools import wraps
from flask_login import current_user
from flask import abort


def only_admin(func):
    @wraps(func)
    def wrapper_decorator(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_admin:
            return func(*args, **kwargs)
        else:
            abort(403)

    return wrapper_decorator
