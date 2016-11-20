import django


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
SECRET_KEY = "secret_key_for_testing"
INSTALLED_APPS = ['django.contrib.auth', 'django.contrib.sites', 'django.contrib.sessions', 'django.contrib.contenttypes', 'easy_timezones']
GEOIP_DATABASE = 'GeoLiteCity.dat'
ROOT_URLCONF = 'easy_timezones.urls'
TIME_ZONE = 'UTC'
ALLOWED_HOSTS = ["*"]
DEBUG = True

if django.VERSION < (1, 8):
    # satisfy tests in django 1.7
    AUTH_USER_MODEL = 'auth.User'
else:
    AUTH_USER_MODEL = None

if django.VERSION >= (1, 9):
    # satisfy deprecation warning in 1.9 and failure in 1.10
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

if django.VERSION >= (1, 10):
    # use new MIDDLEWARE introduced in 1.10
    MIDDLEWARE = ['django.contrib.sessions.middleware.SessionMiddleware', 'easy_timezones.middleware.EasyTimezoneMiddleware']
else:
    MIDDLEWARE_CLASSES = ['django.contrib.sessions.middleware.SessionMiddleware', 'easy_timezones.middleware.EasyTimezoneMiddleware']
