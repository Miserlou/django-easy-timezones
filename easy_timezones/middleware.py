import django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
import pygeoip
import geoip2.database
import geoip2.errors
import os

from .signals import detected_timezone
from .utils import get_ip_address_from_request, is_valid_ip, is_local_ip


db_loaded = False
db = None
db_v6 = None


def load_db_settings():
    GEOIP_VERSION = getattr(settings, 'GEOIP_VERSION', 1)
    if GEOIP_VERSION not in [1, 2]:
        raise ImproperlyConfigured(
            "GEOIP_VERSION setting is defined, but only versions 1 and 2 "
            "are supported")

    GEOIP_DATABASE = getattr(settings, 'GEOIP_DATABASE', 'GeoLiteCity.dat')
    if not GEOIP_DATABASE:
        raise ImproperlyConfigured(
            "GEOIP_DATABASE setting has not been properly defined.")
    if not os.path.exists(GEOIP_DATABASE):
        raise ImproperlyConfigured(
            "GEOIP_DATABASE setting is defined, but {} does not exist.".format(
                GEOIP_DATABASE)
        )

    #
    # Version 2 databases combine both ipv4 and ipv6 data, so only one
    # database file is used for both
    #
    GEOIPV6_DATABASE = getattr(settings, 'GEOIPV6_DATABASE',
                               'GeoLiteCityv6.dat')
    if GEOIP_VERSION == 1:
        if not GEOIPV6_DATABASE:
            raise ImproperlyConfigured(
                "GEOIPV6_DATABASE setting has not been properly defined.")
        if not os.path.exists(GEOIPV6_DATABASE):
            raise ImproperlyConfigured(
                "GEOIPV6_DATABASE setting is defined, but file does not exist.")

    return (GEOIP_DATABASE, GEOIPV6_DATABASE, GEOIP_VERSION)


load_db_settings()


def load_db():
    GEOIP_DATABASE, GEOIPV6_DATABASE, GEOIP_VERSION = load_db_settings()

    global db
    global db_v6
    global db_loaded

    if GEOIP_VERSION == 1:
        db = pygeoip.GeoIP(GEOIP_DATABASE, pygeoip.MEMORY_CACHE)
        db_v6 = pygeoip.GeoIP(GEOIPV6_DATABASE, pygeoip.MEMORY_CACHE)
    elif GEOIP_VERSION ==2:
        db = geoip2.database.Reader(GEOIP_DATABASE)

    db_loaded = True


def lookup_tz_v1(ip):
    """
    Lookup a timezone for the ip using the v1 database.

    :param ip: the ip address, v4 or v6
    :return:   the timezone

    """
    if not db_loaded:
        if ':' in ip:
            return db_v6.time_zone_by_addr(ip)
        else:
            return db.time_zone_by_addr(ip)


def lookup_tz_v2(ip):
    """
    Lookup a timezone for the ip using the v2 database.

    :param ip: the ip address, v4 or v6
    :return:   the timezone

    """
    if not db_loaded:
        load_db()
    #
    # v2 databases support both ipv4 an ipv6
    #
    try:
        response = db.city(ip)
    except geoip2.errors.AddressNotFoundError:
        return None
    return response.location.time_zone


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

        version = getattr(settings, 'GEOIP_VERSION')

        if not tz:
            # use the default timezone (settings.TIME_ZONE) for localhost
            tz = timezone.get_default_timezone()

            client_ip = get_ip_address_from_request(request)
            ip_addrs = client_ip.split(',')
            for ip in ip_addrs:
                if is_valid_ip(ip) and not is_local_ip(ip):
                    if version == 1:
                        tz = lookup_tz_v1(ip)
                    else:
                        tz = lookup_tz_v2(ip)

        if tz:
            timezone.activate(tz)
            request.session['django_timezone'] = str(tz)
            if getattr(settings, 'AUTH_USER_MODEL', None) and getattr(request, 'user', None):
                detected_timezone.send(sender=get_user_model(), instance=request.user, timezone=tz)
        else:
            timezone.deactivate()

