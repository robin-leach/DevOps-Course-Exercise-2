from functools import wraps
from flask_login import current_user
import os

from entity.user import User
from entity.user_role import UserRole


def require_write_privilege(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        login_disabled = os.getenv('LOGIN_DISABLED').upper() == 'TRUE'
        user: User = current_user
        if (login_disabled or user.get_role() == UserRole.Writer):
            return function(*args, **kwargs)
        else:
            return "Unauthorised", 403
    return wrapper
