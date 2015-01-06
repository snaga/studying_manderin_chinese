from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from studying_mandarin_chinese import settings

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
    q = checkRequestParameter(request, 'q', u'select version()')
    r = None

    print settings.engine
    settings.initialize()

    con = connectDatabase()
    rs = con.execute(q)
    for row in rs:
        if r == None:
            r = str(row) + "\n";
        else:
            r = r + str(row) + "\n";
    disconnectDatabase(con)

    template = loader.get_template('dbquery/dbquery.html')
    context = RequestContext(request, {
        'q': q,
        'r': r,
        'engine': settings.engine,
    })
    return HttpResponse(template.render(context))
