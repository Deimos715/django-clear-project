from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

def _jwt_secure_flag():
    # В dev по http куки с secure=True не поедут
    return not settings.DEBUG

def set_jwt_cookies(response, user):
    refresh = RefreshToken.for_user(user)
    response.set_cookie(
        'access', str(refresh.access_token),
        httponly=True, secure=_jwt_secure_flag(), samesite='Lax', path='/'
    )
    response.set_cookie(
        'refresh', str(refresh),
        httponly=True, secure=_jwt_secure_flag(), samesite='Lax', path='/'
    )
    return response

def clear_jwt_cookies(response):
    response.delete_cookie('access', path='/', samesite='Lax')
    response.delete_cookie('refresh', path='/', samesite='Lax')
    return response
