from functools import wraps
from typing import cast

from django.http import HttpResponseForbidden

from users.models import User

def roles_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = cast(User, request.user)

            if user.role not in allowed_roles:
                return HttpResponseForbidden(
                    'You do not have permission to perform this action.'
                )

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator

