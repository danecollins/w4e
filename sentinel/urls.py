from django.conf.urls import patterns, url
from sentinel import views


urlpatterns = patterns('',
                       url(r'^list/$', views.list_monitors),
                       url(r'^add/$', views.add),
                       url(r'^edit/(?P<id>[\d]+)/$', views.edit),
                       url(r'^delete/(?P<id>[\d]+)/$', views.delete),
                       )
