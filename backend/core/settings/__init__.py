import os

env = os.environ.get('DJANGO_ENV', 'dev')

if env == 'prod':
    from core.settings.prod import *
else:
    from core.settings.dev import *
