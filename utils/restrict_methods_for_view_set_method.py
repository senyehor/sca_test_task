from typing import Iterable

from django.utils.decorators import method_decorator
from rest_framework.exceptions import MethodNotAllowed


def restrict_methods(restricted_methods: Iterable[str], message: str):
    @method_decorator
    def outer_wrapper(method):
        def inner_wrapper(request, *args, **kwargs):
            restricted_methods_in_upper = [
                restricted_method.upper() for restricted_method in restricted_methods
            ]
            if request.method in restricted_methods_in_upper:
                raise MethodNotAllowed(request.method, detail=message)
            return method(request, *args, **kwargs)

        return inner_wrapper

    return outer_wrapper
