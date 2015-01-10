from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^register', views.register, name='register'),
    url(r'^audio', views.audio, name='audio'),
    url(r'^view', views.view, name='view'),
    url(r'^index', views.index, name='index'),
    url(r'^result', views.result, name='result'),
    url(r'^$', views.redirect, name='redirect'),
]
