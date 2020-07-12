from functools import wraps
from flask_login import current_user


def only_admin(feature):
    def decorator(view_function):
        @wraps(view_function)
        def decorated(*args, **kwargs):
            if current_user.is_admin:
                return view_function(*args, **kwargs)
            else:
                abort(403)

        return decorated

    return decorator
