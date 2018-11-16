from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.index),
    url('^register$', views.register),
    url('^login$', views.login),
    url('^success$', views.success),
    url('^reset$', views.reset),
    url('^wall$', views.wall),
]