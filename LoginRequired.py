from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve


class LoginRequired:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request,*args, **kwargs):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path
        resolver_match = resolve(path)
        app_name = resolver_match.app_name
        view_name = resolver_match.view_name

        if request.user.is_authenticated or \
                (hasattr(settings, 'LOGIN_URL') and request.path == settings.LOGIN_URL) or \
                (hasattr(settings, 'LOGIN_EXEMPTED_URLS') and request.path in settings.LOGIN_EXEMPTED_URLS) or \
                (hasattr(settings, 'LOGIN_EXEMPTED_URLS') and view_name in settings.LOGIN_EXEMPTED_URLS) or \
                (hasattr(settings, 'LOGIN_EXEMPTED_APPS')) and app_name in settings.LOGIN_EXEMPTED_APPS:
            return None
        return redirect(settings.LOGIN_URL)