from django.conf.urls import patterns, url
from sentinel import views

urlpatterns = patterns('',
                       url(r'^list/$', views.list),
                       url(r'^add/$', views.add),
                       url(r'^details/(?P<id>[\d]+)/$', views.detail),
                       url(r'^edit/(?P<id>[\d]+)/$', views.edit),
                       )
