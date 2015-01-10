from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'studying_mandarin_chinese.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),
    url(r'^vocabulary/', include('vocabulary.urls')),
    url(r'^dbquery/', include('dbquery.urls')),
    url(r'^$', include('vocabulary.urls')),
)
