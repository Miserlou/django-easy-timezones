from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^without_tz/$', views.without_tz, name="without_tz"),
    url(r'^with_tz/$', views.with_tz, name="with_tz"),
]
