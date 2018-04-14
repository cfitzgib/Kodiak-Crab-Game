from django.shortcuts import render
from django.http import HttpResponse
from .models import Crab, Image, Oocyte, Intermediate, PlaySession, SchoolClass

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the Crab Game index.")

def playImg(request, image_id):
    displayImg = Image.objects.get(pk=image_id)
    return render(request, 'crabgame/playImg.html', {'displayImg': displayImg})
