from functools import wraps
from flask_login import current_user
import os
import logging
from html import escape

from entity.user import User
from entity.user_role import UserRole

log = logging.getLogger('app')


def require_write_privilege(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        login_disabled = os.getenv('LOGIN_DISABLED').upper() == 'TRUE'
        if (login_disabled):
            return function(*args, **kwargs)

        user: User = current_user
        log.debug(
            f'User "{user.get_id()}" has hit an endpoint that requires write priveleges')

        if (user.get_role() == UserRole.Writer):
            log.debug(
                f'User "{user.get_id()}" has write permissions, continuing with request')
            return function(*args, **kwargs)
        else:
            log.debug(
                f'User "{user.get_id()}" does not have write permissions, rejecting the request')
            return "Unauthorised", 403

    return wrapper
