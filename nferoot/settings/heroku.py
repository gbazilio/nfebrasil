import os

from nferoot.settings.base import *


DEBUG = False

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

ACCOUNT_ACTIVATION_DAYS = 1
PHANTOMJS_EXECUTABLE = os.path.join(BASE_DIR, '../bin/phantomjs')
