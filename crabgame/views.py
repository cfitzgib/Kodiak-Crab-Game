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
        photo1 = photos[0]
        return render(request, 'crabgame/playCrabImg.html', {'photos': photos}, {'photo1': photo1})
    return render(request, 'crabgame/index.html')

# view the image of a certain crab and click on the oocytes in the image
def detail(request, image_id):
    photo = Image.objects.get(pk=image_id)
    return render(request, 'crabgame/detail.html', {'photo':photo})

# display the result page after the user have completed a session
def result(request, session_id):
    return render(request, 'crabgame/result.html')


