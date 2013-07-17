from django.conf import settings
from django.utils import timezone
import pytz
import pygeoip

db_loaded = False
db = None

def load_db():
    global db
    db = pygeoip.GeoIP(settings.GEOIP_DATABASE, pygeoip.MEMORY_CACHE)

    global db_loaded
    db_loaded=True

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
            ip = get_client_ip(request)
            if ip == '127.0.0.1':
                ip = '192.81.131.111' # OpenWatch is the center of the universe.
            tz = db.time_zone_by_addr(ip)

        if tz:
            timezone.activate(tz)
        else:
            timezone.deactivate()
