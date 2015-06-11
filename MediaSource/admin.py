from django.contrib import admin

# Register your models here.
from MediaSource.models import WebMVideo,VideoSnippetForm

class video_admin(admin.ModelAdmin):
    list_display = ('size','metadata','action','vote_count')
    list_filter = ['size','metadata','action','vote_count']
    
#class snippet_admin(admin.ModelAdmin):
#    list_display = ('metadata','action')
#    list_filter = ['metadata','action']
    
admin.site.register(WebMVideo,video_admin)
#admin.site.register(VideoSnippetForm,snippet_admin)
