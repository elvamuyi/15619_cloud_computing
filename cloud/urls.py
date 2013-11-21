from django.conf.urls import patterns, include, url
from cloud.view import hello, q1, q2, q3, q4

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cloud.views.home', name='home'),
    # url(r'^cloud/', include('cloud.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', hello),
    url(r'^q1/$', q1),
    url(r'^q2/$', q2),
    url(r'^q3/$', q3),
    url(r'^q4/$', q4),
)
