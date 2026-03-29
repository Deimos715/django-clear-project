from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from .utils_jwt import set_jwt_cookies

User = get_user_model()

class JWTAuthForTemplatesMiddleware(MiddlewareMixin):
    '''
    1) Пытаемся авторизовать по access cookie.
    2) Если access нет/протух, пробуем refresh:
        - подставляем request.user сразу,
        - а в process_response тихо перевыпускаем пару access/refresh.
    '''

    def process_request(self, request):
        # Уже аутентифицирован? Ничего не делаем.
        if getattr(request, 'user', None) and request.user.is_authenticated:
            return None

        auth = JWTAuthentication()
        access  = request.COOKIES.get('access')
        refresh = request.COOKIES.get('refresh')

        # 1) Access
        if access:
            try:
                token = auth.get_validated_token(access) # Проверяет только access
                user  = auth.get_user(token)
                request.user = user
                request._cached_user = user # Важно для login_required
                request._jwt_rotate_user = None
                return None
            except (InvalidToken, AuthenticationFailed):
                pass

        # 2) Refresh (не через JWTAuthentication!)
        if refresh:
            try:
                r = RefreshToken(refresh) # Проверка подписи/срока/типа=refresh
                user_id = r['user_id']
                user = User.objects.get(pk=user_id)
                request.user = user
                request._cached_user = user # Чтобы login_required пропустил сразу
                request._jwt_rotate_user = user # Сигнал перевыпустить куки в ответе
                return None
            except (TokenError, User.DoesNotExist):
                request._jwt_rotate_user = None

        # Иначе останемся AnonymousUser
        return None

    def process_response(self, request, response):
        user = getattr(request, '_jwt_rotate_user', None)
        if user is not None:
            set_jwt_cookies(response, user) # выдаём новый access/refresh
        return response
