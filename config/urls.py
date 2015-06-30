from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
import registration

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'w4e.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
)
