from django.shortcuts import render
from django.http import HttpResponse
from .models import Crab, Image, Oocyte, Intermediate, PlaySession, SchoolClass

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the Crab Game index.")

def playCrabImg(request, crab_sample):
    getCrab = Crab.objects.get(sample_num = crab_sample)
    crabImgs = getCrab.image_set.all()
    displayImg = crabImgs[0] # eventually this will be a random number within the size of the set (crabImgs.count())
    return render(request, 'crabgame/playCrabImg.html', {'displayImg': displayImg})
