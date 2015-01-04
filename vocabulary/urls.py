from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^', views.register, name='register'),
]
