DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
SECRET_KEY = "secret_key_for_testing"
INSTALLED_APPS = ['django.contrib.auth', 'django.contrib.sites', 'django.contrib.sessions', 'django.contrib.contenttypes', 'easy_timezones']
MIDDLEWARE_CLASSES = ['django.contrib.sessions.middleware.SessionMiddleware', 'easy_timezones.middleware.EasyTimezoneMiddleware']
GEOIP_DATABASE = 'GeoLiteCity.dat' 
ROOT_URLCONF = 'easy_timezones.urls'
TIME_ZONE = 'UTC'
ALLOWED_HOSTS = ["*"]
DEBUG = True
AUTH_USER_MODEL = None
