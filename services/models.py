from django.db import models
from filey.settings import AUTH_USER_MODEL


class Link(models.Model):

    '''Model containing `user` uploaded file path.'''
    link = models.FileField(upload_to='filey/users/')
    is_accessible = models.BooleanField(default=False, blank=True)
    is_downloadable = models.BooleanField(default=False, blank=True)


class Item(models.Model):

    '''Model containing the name and owner of uploaded content in `Link` model'''
    name = models.CharField(max_length=60, blank=True)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    link = models.OneToOneField('Link', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
