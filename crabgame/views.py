from django.shortcuts import render
from django.http import HttpResponse
from django.core.files import File
import os
from .models import Crab, Image, Oocyte, Intermediate, PlaySession, SchoolClass

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the Crab Game index.")

def playImg(request, image_id):
    displayImg = Image.objects.get(pk=4)
    content = displayImg.read()
    return HttpResponse(content)
    return HttpResponse("You're looking at image # %s" % image_id)