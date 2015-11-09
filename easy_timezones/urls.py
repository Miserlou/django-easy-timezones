from django.conf.urls import url

urlpatterns = [
    url(r'^without_tz/$', 'easy_timezones.views.without_tz', name="without_tz"),
    url(r'^with_tz/$', 'easy_timezones.views.with_tz', name="with_tz"),
]