# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from studying_mandarin_chinese import settings

import httplib
import urllib
from models import Word
from models import pinyin

def checkRequestParameter(req, key, default):
    val = None

    if key in req.GET:
        val = req.GET[key]
    elif key in req.POST:
        val = req.POST[key]
    else:
        val = default

    return val

def connectDatabase():
    return settings.engine[0].connect()

def disconnectDatabase(conn):
    conn.close()

# Create your views here.
def register(request):
    q = checkRequestParameter(request, 'q', u'你好')

    print settings.engine
    settings.initialize()

    con = connectDatabase()
    result = con.execute("select version()")
    for row in result:
        version = row['version']
    disconnectDatabase(con)

    w = Word(q, pinyin(q), None)

    print("q = " + q.encode('utf-8'))

    template = loader.get_template('vocabulary/register.html')
    context = RequestContext(request, {
        'w': w,
        'engine': settings.engine,
        'version': version,
    })
    return HttpResponse(template.render(context))
