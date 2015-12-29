import django
DJANGO_18_PLUS = django.VERSION[:2] >= (1, 8)
DJANGO_18_PLUS_APPS = ['django.contrib.auth', 'django.contrib.contenttypes']
DJANGO_APPS_ALL_VERSIONS = ['django.contrib.sessions', 'easy_timezones']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
SECRET_KEY = "secret_key_for_testing"
MIDDLEWARE_CLASSES = ['django.contrib.sessions.middleware.SessionMiddleware', 'easy_timezones.middleware.EasyTimezoneMiddleware']
GEOIP_DATABASE = 'GeoLiteCity.dat' 
ROOT_URLCONF = 'easy_timezones.urls'
DEBUG = True
TIME_ZONE = 'UTC'
ALLOWED_HOSTS = ["*"]
AUTH_USER_MODEL = None

if DJANGO_18_PLUS:
	INSTALLED_APPS = DJANGO_18_PLUS_APPS + DJANGO_APPS_ALL_VERSIONS
	TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates'}]
else:
	INSTALLED_APPS = DJANGO_APPS_ALL_VERSIONS
