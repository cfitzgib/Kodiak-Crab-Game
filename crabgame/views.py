from django.shortcuts import render
from django.http import HttpResponse
from .models import Crab, Image, Oocyte, Intermediate, PlaySession, SchoolClass
import random
import json

# Create your views here.

# if start start button clicked, create instance of PlaySession and get 12 random photos to play 
def index(request):
    if request.method == 'POST':
        playSessionInstance = PlaySession()
        playSessionInstance.save()
        photos = playSessionInstance.setPhotos()
        photo1 = photos[0]
        for i in range (0, len(photos)):
            displayImg = photos[i]
            return render(request, 'crabgame/playCrabImg.html', {'photos': enumerate(photos)})
    return render(request, 'crabgame/index.html')

#Gets data from ajax request, finds oocyte clicked,
#and passes this back as a JSON response
def find_oocyte(request):
    x, y = request.GET.get('xclick'), request.GET.get('yclick')
    photoid = request.GET.get('photoid')
    photo = Image.objects.get(pk=photoid)
    clicked_oocyte = photo.find_closest_oocyte(x, y)
    resp = { 'xcenter': clicked_oocyte.center_x, 'ycenter': clicked_oocyte.center_y, 'id': clicked_oocyte.id }
    return HttpResponse(json.dumps(resp), content_type="application/json")

def increment_oocyte(request):
    oocyte_id = request.GET.get('id')
    Oocyte.objects.get(pk=oocyte_id).increment_chosen_count()
    return HttpResponse()
     
# view the image of a certain crab and click on the oocytes in the image
def detail(request, image_id):
    photo = Image.objects.get(pk=image_id)
    return render(request, 'crabgame/detail.html', {'photo':photo})

# display the result page after the user have completed a session
def result(request, session_id):
    return render(request, 'crabgame/result.html')


