from time import time

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'', include('profile.urls')),
    url(r'dvesto/', include('dennych_dvesto.urls')),
    url(r'basen/', include('nocna_basen.urls')),
)


