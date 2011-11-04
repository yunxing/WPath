# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
import getPath


def index(request):
    t = loader.get_template('index/index.html')
    c = Context({
    })
    return HttpResponse(t.render(c))

def test(request):
    t = loader.get_template('index/test.html')
    l = getPath.getNeighbor("yahoo")
    c = Context({
            'nodelist': l,
    })
    return HttpResponse(t.render(c))
