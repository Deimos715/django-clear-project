import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Секретный ключ
SECRET_KEY = os.getenv('SECRET_KEY')


# Sita id
SITE_ID = 1


# CSRF домены
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin.strip()
]


# Своя модель пользователя
AUTH_USER_MODEL = 'account.CustomUser'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # user apps
    'src.main.apps.MainConfig',
    'src.seo.apps.SeoConfig',
    'src.account.apps.AccountConfig',
    'src.lk.apps.LkConfig',

    # Other apps
    'rest_framework',
    'rest_framework_simplejwt',

    # sitemaps
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # robots
    'robots',
]


# Сессии/сообщения не в БД (только cookie)
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# JWT настройки
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'LEEWAY': 30,
}


# Cookies
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'


# AUTHENTICATION_BACKENDS определяет список бэкендов аутентификации, которые Django будет использовать
# 'django.contrib.auth.backends.ModelBackend' — стандартный бэкенд Django,
# который проверяет учетные данные (email/username + пароль) через модель пользователя,
# а также обрабатывает права доступа (is_active, is_staff, is_superuser, группы, разрешения).
# Если в списке оставить только этот бэкенд, вход возможен только через пользователей,
# хранящихся в базе Django, без сторонних систем авторизации.
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'src.seo.context_processors.seo_data',  # Контекстный процессор Seo
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database SQLite, для режима development (расскоментировать при зобычном запуске с SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgreSQL, для режима development/production (расскоментировать при запуске через Docker
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('DB_HOST'),
#         'PORT': os.getenv('DB_PORT'),
#     }
# }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    # Стандартные валидаторы паролей Django отключены, так как используются кастомные валидаторы
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # Отключен, так как используется кастомный валидатор
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },

    # Кастомные валидаторы паролей
    {
        'NAME': 'src.account.validators.CustomMinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
]


# Internationalization
LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'


# Directory definition for static
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# Defining the base directory for collecting staticfiles
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# URL-имя (name из urls.py), на который Django будет перенаправлять
# незалогиненного пользователя при попытке доступа к @login_required вьюхе.
# Django автоматически добавит параметр ?next=... для возврата после входа.
LOGIN_URL = 'account:login'


# URL-имя, куда Django отправит пользователя после успешного входа,
# если в запросе не был передан параметр next.
# Используется, например, во встроенном LoginView или при ручном redirect().
# Пока на main:index
LOGIN_REDIRECT_URL = 'lk:profile'


# Настройки для отправки почты
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.mail.ru')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 465))
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'True') == 'True'
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'False') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_TIMEOUT = 20
