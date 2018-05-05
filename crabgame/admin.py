from django.contrib import admin
from .models import Crab, Image, Oocyte, PlaySession, PlaySessionImage

# Register your models here.
admin.site.register(Crab)
admin.site.register(Image)
admin.site.register(Oocyte)
admin.site.register(PlaySession)
admin.site.register(PlaySessionImage)