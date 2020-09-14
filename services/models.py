from django.db import models
from filey.settings import AUTH_USER_MODEL


class Item(models.Model):
    
    '''Model containing the name and owner of uploaded content in `Link` model'''
    name = models.CharField(max_length=60, blank=True)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    file = models.FileField(upload_to='filey/users/')
    is_accessible = models.BooleanField(default=False, blank=True)
    is_downloadable = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        
        '''deletes old file when making an update to file'''
        try:
            old = Item.objects.get(id=self.id)
            if old.file != self.file:
                old.file.delete(save=False)
        except:
            pass
        super(Item, self).save(*args, **kwargs)
