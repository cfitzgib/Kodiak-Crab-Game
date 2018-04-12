from django.contrib import admin
from .models import Crab, Image, Oocyte, Intermediate, PlaySession, SchoolClass

# Register your models here.
admin.site.register(Crab)
admin.site.register(Image)
admin.site.register(Oocyte)
admin.site.register(Intermediate)
admin.site.register(PlaySession)
admin.site.register(SchoolClass)
