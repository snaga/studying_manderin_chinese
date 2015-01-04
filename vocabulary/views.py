# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from studying_mandarin_chinese import settings

from xpinyin import Pinyin
import httplib
import urllib

def pinyin(s):
    p = Pinyin()
    s2 = p.get_pinyin(unicode(s), ' ', show_tone_marks=True)
    return s2

# Create your views here.
def register(request):
    if 'q' in request.POST:
        q = request.POST['q']
    else:
        q = u'你好'

    print settings.engine
    settings.initialize()

    print("q = " + q.encode('utf-8'))

    template = loader.get_template('vocabulary/register.html')
    context = RequestContext(request, {
        'q': q,
        'p': pinyin(q).encode('utf-8'),
        'engine': settings.engine,
    })
    return HttpResponse(template.render(context))
