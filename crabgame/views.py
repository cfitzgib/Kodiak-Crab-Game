from django.shortcuts import render
from django.http import HttpResponse
from .models import Crab, Image, Oocyte, Intermediate, PlaySession, SchoolClass
import random

# Create your views here.

# if start start button clicked, create instance of PlaySession and get 12 random photos to play 
def index(request):
    if request.method == 'POST':
        playSessionInstance = PlaySession()
        playSessionInstance.save()
        photos = playSessionInstance.setPhotos()
        for i in range (0, len(photos)):
            displayImg = photos[i]
            return render(request, 'crabgame/playCrabImg.html', {'photos': photos})
    return render(request, 'crabgame/index.html')


