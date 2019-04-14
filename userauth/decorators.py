from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

def permission_check_admin(function):
    def wrapper(request, **kwargs):
        user = request.user
        if user is not None and user.is_authenticated and user.is_staff:
            return function(request, **kwargs)
        else:
            return HttpResponseRedirect(reverse('userauth:customer_logout'))
    return wrapper
