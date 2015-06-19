'''
Created on Apr 16, 2015

@author: ronaldjosephdesmarais
'''
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from MediaSource import views

urlpatterns = patterns('',
    # Examples: (?P<video_id>[0-9]+)
    url(r'^$', views.home, name='home'),
    url(r'^video_snippet', views.video_snippet ,name='video snip'),
    url(r'^video_vote', views.video_vote ,name='video vote'),
    url(r'^video_stream/(?P<video_id>[0-9]+)', views.video_stream ,name='video stream'),
    url(r'^video_submit_vote/(?P<video_id>[0-9]+)/(?P<video_submit_vote>\d)', views.video_submit_vote ,name='video stream'),
    
    #returns video at index of videos sorted by likes
    url(r'^video_stream_count/(?P<video_index>[0-9]+)', views.video_stream_count ,name='video stream by count'), 
    url(r'^admin/', include(admin.site.urls)),
    
)
