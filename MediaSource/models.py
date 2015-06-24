from django.db import models

# Create your models here.
from django import forms

import base64


class WebMVideo(models.Model):

    size = models.IntegerField()
    metadata = models.CharField(max_length=200)
    action = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    vote_count = models.IntegerField()
    
    _data = models.TextField(
            db_column='data',
            blank=True)
    
    _img_data = models.TextField(
            db_column='image data',
            blank=True)

    def set_data(self, data, image_data, metadata, action,message):
        self._data = data
        self._img_data = image_data
        self.metadata=metadata
        self.action=action
        self.size=len(data)
        self.message=message
        self.vote_count=0

    def get_data(self):
        return self._data
 
    def get_image_data(self):
        return self._img_data

    data = property(get_data, set_data)
    
    
class VideoSnippetForm(forms.Form):
    metadata = forms.CharField(max_length=100)
    action = forms.CharField()
    message = forms.CharField()
    