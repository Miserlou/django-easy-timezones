![Timezones. Yuck.](http://i.imgur.com/Qc2W47H.gif)

django-easy-timezones
=====================

Easy timezones for Django (>=1.4) based on MaxMind GeoIP.

Quick start
-----------

1. Install django-easy-timezones

    ```python
    pip install django-easy-timezones
    ```

1. Add "easy-timezones" to your INSTALLED_APPS setting like this:

    ```python
    INSTALLED_APPS = (
      ...
      'easy_timezones',
    )
    ```

1. Add EasyTimezoneMiddleware to your MIDDLEWARE_CLASSES 

    ```python
    MIDDLEWARE_CLASSES = (
      ...
      'easy_timezones.middleware.EasyTimezoneMiddleware',
    )
    ```

1. Add a path to the [MaxMind GeoIP database](http://www.maxmind.com/en/geolocation_landing) ([direct
link](https://raw.github.com/Miserlou/django-easy-timezones/master/GeoIP.dat) because I'm nice) in your settings file:

    ```python
    GEOIP_DATABASE = '/path/to/your/geoip/database/GeoIP.dat'
    ```

1. Enable localtime in your templates.

    ```python
    {% load tz %}
        The UTC time is {{ object.date }}
    {% localtime on %}
        The local time is {{ object.date }}
    {% endlocaltime %}
    ```
    
1. To hook into the Timezone detection event to, say, save it to the request's user somewhere more permanent than a session, do something like this:

	```python
	from easy_timezones.signals import detected_timezone	

	@receiver(detected_timezone, sender=MyUserModel)
	def process_timezone(sender, instance, timezone, **kwargs):
    	if instance.timezone != timezone:
        	instance.timezone = timezone
        	instance.save()
	```

1. Twist one up, cause you're done, homie!
