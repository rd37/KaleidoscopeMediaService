from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.conf.urls.static import static
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'KaleidoscopeMediaService.views.home', name='home'),
    url(r'^mediasource/', include('MediaSource.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
