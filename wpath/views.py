# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
import getPath
import shelve
db = shelve.open('cache.db')

def index(request):
    l = db["index"] 
    return render_to_response('index/example2.html', {'nodelist': l},
                               context_instance=RequestContext(request))

def test(request):
    start = request.POST['start']
    end = request.POST['end']    
    l = getPath.getPath(start, end)
    return render_to_response('index/example2.html', {'nodelist': l},
                               context_instance=RequestContext(request))    
