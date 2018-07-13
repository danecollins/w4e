from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from sentinel import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'w4e.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/beta/', views.beta),
    url(r'^accounts/contact/', views.contact),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^sentinels/', include('sentinel.urls')),
    url(r'^checkin/(?P<tag>.*)[/]*$', views.checkin),
    url(r'^events/history/$', views.event_history),
    url(r'^faq/', TemplateView.as_view(template_name="faq.html"))
]
