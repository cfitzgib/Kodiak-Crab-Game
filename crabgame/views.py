from django.shortcuts import render
from django.http import HttpResponse
from .models import Crab, Image, Oocyte, Intermediate, PlaySession, SchoolClass
import random

# Create your views here.

def index(request):
    if request.method == 'POST':
        playSessionInstance = PlaySession()
        playSessionInstance.save()
        playCrabImg(request, playSessionInstance)
    return render(request, 'crabgame/index.html')

# def playCrabImg(request, crab_sample):
#     getCrab = Crab.objects.get(sample_num = crab_sample) # get a crab with a specified sample num
#     crabImgs = getCrab.image_set.all() # get all the image instances for that specific crab
#     displayImg = random.choice(crabImgs) # choose a random image instance to display from that crab
#     return render(request, 'crabgame/playCrabImg.html', {'displayImg': displayImg})

def playCrabImg(request, playSessionInstance):
    photos = playSessionInstance.setPhotos()
    for i in range (0, len(photos)):
        displayImg = photos[i]
        return render(request, 'crabgame/playCrabImg.html', {'displayImg': displayImg})
