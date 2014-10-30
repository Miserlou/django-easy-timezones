from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
import pytz
import pygeoip

from .signals import detected_timezone
from .utils import get_ip_address_from_request


GEOIP_DATABASE_IPV4 = getattr(settings, 'GEOIP_DATABASE_IPV4', None)
GEOIP_DATABASE_IPV6 = getattr(settings, 'GEOIP_DATABASE_IPV6', None)

if not GEOIP_DATABASE_IPV4 or not GEOIP_DATABASE_IPV6:
    raise ImproperlyConfigured("GEOIP_DATABASE setting has not been defined.")


db_ipv4_loaded = False
db_ipv6_loaded = False
db_ipv4 = None
db_ipv6 = None

def load_db():
    global db_ipv4, db_ipv6
    db_ipv4 = pygeoip.GeoIP(GEOIP_DATABASE_IPV4, pygeoip.MEMORY_CACHE)
    db_ipv6 = pygeoip.GeoIP(GEOIP_DATABASE_IPV6, pygeoip.MEMORY_CACHE)

    global db_ipv4_loaded, db_ipv6_loaded
    db_ipv4_loaded, db_ipv6_loaded = True, True


class EasyTimezoneMiddleware(object):
    def process_request(self, request):
        if not db_ipv4_loaded or not db_ipv6_loaded:
            load_db()

        tz = request.session.get('django_timezone')

        if not tz:
            # use the default timezone (settings.TIME_ZONE) for localhost
            tz = timezone.get_default_timezone()

            ip = get_ip_address_from_request(request)
            if ip != '127.0.0.1':
                # if not local, fetch the timezone from pygeoip
                tz = db_ipv4.time_zone_by_addr(ip)
                if tz == None:
                    tz = db_ipv6.time_zone_by_addr(ip)

        if tz:
            timezone.activate(tz)
            detected_timezone.send(sender=get_user_model(), instance=request.user, timezone=tz)
        else:
            timezone.deactivate()
