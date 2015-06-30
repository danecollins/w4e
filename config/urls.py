from django.conf.urls import patterns, include, url
from django.contrib import admin
from sentinel import views
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'w4e.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^sentinels/', include('sentinel.urls')),
    url(r'^checkin/(?P<tag>.*)[/]*$', views.checkin),
    url(r'^events/history/$', views.event_history),
)
