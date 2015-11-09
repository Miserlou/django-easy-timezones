DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
SECRET_KEY = "secret_key_for_testing"
INSTALLED_APPS = ['easy_timezones']
MIDDLEWARE_CLASSES = ['easy_timezones.middleware.EasyTimezoneMiddleware']
GEOIP_DATABASE = 'GeoLiteCity.dat' 
