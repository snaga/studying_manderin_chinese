# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import RequestContext, loader
from studying_mandarin_chinese import settings

import httplib
import urllib
from models import Word
from models import pinyin
import binascii

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

def registerWord(w):
    con = connectDatabase()
    query = "insert into word values ('" + w.hanji + "', '" + w.pinyin + "', E'\\\\x" + w.audio + "'::bytea, '" + w.ja + "')"
    print("query: " + query.encode('utf-8'))
    result = con.execute(query)
    disconnectDatabase(con)

def findWord(hanji):
    print settings.engine
    settings.initialize()

    con = connectDatabase()

    query = "SELECT hanji,pinyin,audio,ja FROM word WHERE hanji = '" + hanji + "'";
    print("query: " + query.encode('utf-8'))
    rs = con.execute(query)
    w = None
    for row in rs:
        w = Word(row['hanji'], row['pinyin'], row['audio'], row['ja'])

    disconnectDatabase(con)
    return w

def findNextWord(hanji):
    print settings.engine
    settings.initialize()

    con = connectDatabase()

    query = "SELECT hanji FROM word WHERE hanji > '" + hanji + "' ORDER BY hanji LIMIT 1";
    print("query: " + query.encode('utf-8'))
    rs = con.execute(query)

    # in case reaching the end of the list
    if rs.rowcount == 0:
        query = "SELECT hanji FROM word ORDER BY hanji LIMIT 1";
        print("query: " + query.encode('utf-8'))
        rs = con.execute(query)

    w = None
    for row in rs:
        w = row['hanji']

    disconnectDatabase(con)
    return w

def allWords():
    word_list = []

    print settings.engine
    settings.initialize()

    con = connectDatabase()

    query = "SELECT hanji,pinyin,audio,ja FROM word";
    print("query: " + query.encode('utf-8'))
    rs = con.execute(query)
    w = None
    for row in rs:
        w = Word(row['hanji'], row['pinyin'], row['audio'], row['ja'])
        word_list.append(w)
    disconnectDatabase(con)

    return word_list

def index(request):
    word_list = allWords()

    template = loader.get_template('vocabulary/index.html')
    context = RequestContext(request, {
        'word_list': word_list,
    })

    return HttpResponse(template.render(context))

# Create your views here.
def register(request):
    q = checkRequestParameter(request, 'q', u'你好')
    ja = checkRequestParameter(request, 'ja', u'こんにちわ')

    if request.method == 'POST' and 'audio' in request.FILES:
        audio = ""
        for chunk in request.FILES['audio'].chunks():
            if audio == None:
                audio = binascii.b2a_hex(chunk)
            else:
                audio = audio + binascii.b2a_hex(chunk)

        print settings.engine
        settings.initialize()

        w = Word(q, pinyin(q), audio, ja)

        registerWord(w)
    else:
        w = Word(q, pinyin(q), None, None)

    print("q = " + q.encode('utf-8'))

    template = loader.get_template('vocabulary/register.html')
    context = RequestContext(request, {
        'w': w,
        'engine': settings.engine,
    })
    return HttpResponse(template.render(context))

def view(request):
    q = checkRequestParameter(request, 'q', u'你好')

    w = findWord(q)
    if w == None:
        return HttpResponseNotFound('<h1>' + q + ' not found</h1>')

    template = loader.get_template('vocabulary/view.html')
    context = RequestContext(request, {
        'w': w,
        'engine': settings.engine,
    })
    return HttpResponse(template.render(context))

def result(request):
    q = checkRequestParameter(request, 'q', None)

    w = findNextWord(q)

    return HttpResponsePermanentRedirect("/vocabulary/view?q=" + w)

def audio(request):
    q = checkRequestParameter(request, 'q', u'你好')

    w = findWord(q)
    if w == None:
        return HttpResponseNotFound('<h1>' + q + ' not found</h1>')

    resp = HttpResponse(w.audio, mimetype='audio/mp3')
    resp['Content-Disposition'] = 'attachment; filename=audio.mp3'

    return resp

def redirect(request):
    return HttpResponseRedirect("/vocabulary/index")
