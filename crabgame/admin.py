from django.contrib import admin
from .models import Crab, Image, Oocyte, PlaySession

# Register your models here.
admin.site.register(Crab)
admin.site.register(Image)
admin.site.register(Oocyte)
admin.site.register(PlaySession)