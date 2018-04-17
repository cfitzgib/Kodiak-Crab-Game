from django.shortcuts import render
from django.http import HttpResponse
from .models import Crab, Image, Oocyte, Intermediate, PlaySession, SchoolClass
import random

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the Crab Game index.")

def playCrabImg(request, crab_sample):
    getCrab = Crab.objects.get(sample_num = crab_sample) # get a crab with a specified sample num
    crabImgs = getCrab.image_set.all() # get all the image instances for that specific crab
    displayImg = random.choice(crabImgs) # choose a random image instance to display from that crab
    return render(request, 'crabgame/playCrabImg.html', {'displayImg': displayImg})
