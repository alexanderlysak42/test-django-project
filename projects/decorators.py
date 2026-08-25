from functools import wraps
from typing import cast

from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden

from users.models import User

def roles_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())

            user = cast(User, request.user)

            if user.role not in allowed_roles:
                return HttpResponseForbidden(
                    'You do not have permission to perform this action.'
                )

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator

