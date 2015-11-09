from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
import pytz
import pygeoip
import os

from .signals import detected_timezone
from .utils import get_ip_address_from_request, is_valid_ip

db_loaded = False
db = None

def load_db_settings():
    GEOIP_DATABASE = getattr(settings, 'GEOIP_DATABASE', 'GeoLiteCity.dat')

    if not GEOIP_DATABASE:
        raise ImproperlyConfigured("GEOIP_DATABASE setting has not been properly defined.")

    if not os.path.exists(GEOIP_DATABASE):
        raise ImproperlyConfigured("GEOIP_DATABASE setting is defined, but file does not exist.")

    return GEOIP_DATABASE

load_db_settings()

def load_db():

    global db
    db = pygeoip.GeoIP(settings.GEOIP_DATABASE, pygeoip.MEMORY_CACHE)

    global db_loaded
    db_loaded = True

class EasyTimezoneMiddleware(object):
    def process_request(self, request):

        if not request:
            return

        if not db_loaded:
            load_db()

        tz = request.session.get('django_timezone')

        if not tz:
            # use the default timezone (settings.TIME_ZONE) for localhost
            tz = timezone.get_default_timezone()

            client_ip = get_ip_address_from_request(request)
            ip_addrs = client_ip.split(',')
            for ip in ip_addrs:
                if is_valid_ip(ip) and ip != '127.0.0.1':
                    tz = db.time_zone_by_addr(ip)
                    break

        if tz:
            timezone.activate(tz)
            detected_timezone.send(sender=get_user_model(), instance=request.user, timezone=tz)
        else:
            timezone.deactivate()
