from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Template, Context

from datetime import datetime

def with_tz(request):
    """
    Get the time with TZ enabled

    """
    
    dt = datetime.now() 
    t = Template('{% load tz %}{% localtime on %}{% get_current_timezone as TIME_ZONE %}{{ TIME_ZONE }}{% endlocaltime %}') 
    c = RequestContext(request)
    response = t.render(c)
    return HttpResponse(response)

def without_tz(request):
    """
    Get the time without TZ enabled

    """
    
    t = Template('{% load tz %}{% get_current_timezone as TIME_ZONE %}{{ TIME_ZONE }}') 
    c = RequestContext(request)
    response = t.render(c)
    return HttpResponse(response)