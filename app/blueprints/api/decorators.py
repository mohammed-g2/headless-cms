from functools import wraps
from flask import abort, g
from app.models import Permission
from .authentication import auth


def permission_required(permission: int):
    """abort with 403 if current user doesn't have given permission"""
    def decorator(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            if not g.current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_func
    return decorator


def admin_required(f):
    """abort with 403 if current user is not admin"""
    return permission_required(Permission.ADMIN)(f)
