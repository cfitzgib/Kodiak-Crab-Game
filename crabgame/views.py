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
        total = len(photos)
        return render(request, 'crabgame/playCrabImg.html', {'photos': enumerate(photos), 'total': total, 'session_id': playSessionInstance.id})
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
    session = PlaySession.objects.get(pk=session_id)
    analyzedCrabs = session.getCrabs()
    crabCount = len(analyzedCrabs)
    return render(request, 'crabgame/result.html', {'analyzedCrabs': enumerate(analyzedCrabs), 'crabCount': crabCount})

# Remove crabs that have reached done_oocytes count 
def remove_crabs(request, session_id):
    crab_ids = request.GET.get('crab_ids')
    crab_ids = set(crab_ids.split(","))
    for elem in crab_ids:
        crab_id = int(elem)
        crab = Crab.objects.get(pk=crab_id)
        print("The crab pk is " + str(crab_id))
        if crab.done_oocytes >= 10:
            crab.delete()
    return HttpResponse()



