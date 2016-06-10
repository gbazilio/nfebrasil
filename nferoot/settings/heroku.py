from nferoot.settings.base import *


DEBUG = False

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

PHANTOMJS_EXECUTABLE = os.path.join(BASE_DIR, '../bin/phantomjs')

# export DATABASE_URL=postgres:///$(whoami)
DATABASES = {
    'default': dj_database_url.config()
}
