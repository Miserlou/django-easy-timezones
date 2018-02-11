import django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
import pytz
import pygeoip
import os
from pathlib import Path

from .signals import detected_timezone
from .utils import get_ip_address_from_request, is_valid_ip, is_local_ip

db_loaded = False
db = None
db_v6 = None



def load_db_settings():
    """Loads the db settings. Checks in the django settings for the paths to the GEOIP and
    GEOIPV6 databases. If not found it uses the default databases"""

    # Default database paths
    current_dir = Path(__file__).parent
    GEOIP_DEFAULT_DATABASE = current_dir / 'GeoLiteCity.dat'
    GEOIPV6_DEFAULT_DATABASE = current_dir / 'GeoLiteCityv6.dat'

    # Loading the settings
    GEOIP_DATABASE = getattr(settings, 'GEOIP_DATABASE', GEOIP_DEFAULT_DATABASE)

    if not GEOIP_DATABASE:
        raise ImproperlyConfigured("GEOIP_DATABASE setting has not been properly defined.")

    if not os.path.exists(GEOIP_DATABASE):
        raise ImproperlyConfigured("GEOIP_DATABASE setting is defined, but file does not exist.")

    GEOIPV6_DATABASE = getattr(settings, 'GEOIPV6_DATABASE', GEOIPV6_DEFAULT_DATABASE)

    if not GEOIPV6_DATABASE:
        raise ImproperlyConfigured("GEOIPV6_DATABASE setting has not been properly defined.")

    if not os.path.exists(GEOIPV6_DATABASE):
        raise ImproperlyConfigured("GEOIPV6_DATABASE setting is defined, but file does not exist.")

    return (GEOIP_DATABASE, GEOIPV6_DATABASE)

load_db_settings()

def load_db():

    GEOIP_DATABASE, GEOIPV6_DATABASE = load_db_settings()

    global db
    db = pygeoip.GeoIP(GEOIP_DATABASE, pygeoip.MEMORY_CACHE)

    global db_v6
    db_v6 = pygeoip.GeoIP(GEOIPV6_DATABASE, pygeoip.MEMORY_CACHE)

    global db_loaded
    db_loaded = True


if django.VERSION >= (1, 10):
    from django.utils.deprecation import MiddlewareMixin
    middleware_base_class = MiddlewareMixin
else:
    middleware_base_class = object


class EasyTimezoneMiddleware(middleware_base_class):
    def process_request(self, request):
        """
        If we can get a valid IP from the request,
        look up that address in the database to get the appropriate timezone
        and activate it.

        Else, use the default.

        """

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
                if is_valid_ip(ip) and not is_local_ip(ip):
                    if ':' in ip:
                        tz = db_v6.time_zone_by_addr(ip)
                        break
                    else:
                        tz = db.time_zone_by_addr(ip)
                        break

        if tz:
            timezone.activate(tz)
            request.session['django_timezone'] = str(tz)
            if getattr(settings, 'AUTH_USER_MODEL', None) and getattr(request, 'user', None):
                detected_timezone.send(sender=get_user_model(), instance=request.user, timezone=tz)
        else:
            timezone.deactivate()
