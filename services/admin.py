from django.contrib import admin
from services.models import Link, Item
# Register your models here.

admin.site.register((Link, Item))
# admin.site.register(Item)