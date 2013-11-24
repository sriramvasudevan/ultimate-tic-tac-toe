from django.conf.urls import patterns, url

from UTTTApp import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^getmove/$', views.getMove, name='getMove'),
)
