from isin.settings import *

AUTHENTICATION_BACKENDS = (
    # 'django_cas.backends.CASBackend',
    'django.contrib.auth.backends.ModelBackend',
)
