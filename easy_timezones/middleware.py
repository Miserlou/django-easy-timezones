from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
import pytz
import pygeoip

from .signals import detected_timezone

db_loaded = False
db = None

def load_db():
    global db
    db = pygeoip.GeoIP(settings.GEOIP_DATABASE, pygeoip.MEMORY_CACHE)

    global db_loaded
    db_loaded = True

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip

class EasyTimezoneMiddleware(object):
    def process_request(self, request):
        if not db_loaded:
            load_db()

        tz = request.session.get('django_timezone')

        if not tz:
            # use the default timezone (settings.TIME_ZONE) for localhost
            tz = timezone.get_default_timezone()

            ip = get_client_ip(request)
            if ip != '127.0.0.1':
                # if not local, fetch the timezone from pygeoip
                tz = db.time_zone_by_addr(ip)

        if tz:
            timezone.activate(tz)
            detected_timezone.send(sender=get_user_model(), instance=request.user, timezone=tz)
        else:
            timezone.deactivate()
