from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from studying_mandarin_chinese import settings
import os

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
def dbquery(request):
    token = checkRequestParameter(request, 'DBQUERY_TOKEN', None)
    q = checkRequestParameter(request, 'q', '')
    r = None

    print settings.engine
    settings.initialize()

    print("token: " + str(os.getenv("DBQUERY_TOKEN")) + "," + str(token))

    msg = ""
    if len(q) > 0 and token == os.getenv("DBQUERY_TOKEN"):
        con = connectDatabase()
        rs = con.execute(q)
        for row in rs:
            if r == None:
                r = str(row) + "\n";
            else:
                r = r + str(row) + "\n";
        disconnectDatabase(con)
    elif len(q) > 0:
        msg = "token error."

    template = loader.get_template('dbquery/dbquery.html')
    context = RequestContext(request, {
        'msg': msg,
        'token': token,
        'q': q,
        'r': r,
        'engine': settings.engine,
    })
    return HttpResponse(template.render(context))
