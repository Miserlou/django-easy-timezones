# Django
import django.dispatch

detected_timezone = django.dispatch.Signal(providing_args=["instance", "timezone"])
