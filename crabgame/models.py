from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.core.files import File
import datetime
import random
import os, json
import csv
import re
import math
from sodapy import Socrata
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Crab(models.Model):
    sample_num = models.IntegerField(default = 0) # used to find the crab image
    # number of oocytes that reached more than 10 clicks
    done_oocytes = models.IntegerField(default = 0, validators = [MaxValueValidator(10)])
    year = models.IntegerField(default = datetime.date.today().year)
    latitude = models.FloatField()
    longitude = models.FloatField()
    water_temp = models.FloatField() 
    shell_condition = models.IntegerField()

    #Called by a crab when it has 10 completed oocytes. It will then send its data to socrata.
    def send_crab_data(self):
        CONVERSION_RATE = .00000701549
        oocytes = Oocyte.objects.filter(crab=self).filter(chosen_count=10)
        client = Socrata("noaa-fisheries-afsc.data.socrata.com", "q3DhSQxvyWbtq1kLPs5q7jwQp",  username="cfitzgib@andrew.cmu.edu", password = "Kodiak18!")
        data = {'area_2': '',
                 'area_5': '', 
                 'calibration_5x': 0.00028, 
                 'area_4': '', 
                 'area_7': '', 
                 'area_10': '', 
                 'calibration_10x': 0.00056, 
                 'area_9': '', 
                 'year': '', 
                 'sample': '', 
                 'area_3': '', 
                 'area_8': '', 
                 'area_1': '', 
                 'area_6': ''}
        data['area_1'] = oocytes[0].area * CONVERSION_RATE
        data['area_2'] = oocytes[1].area * CONVERSION_RATE
        data['area_3'] = oocytes[2].area * CONVERSION_RATE
        data['area_4'] = oocytes[3].area * CONVERSION_RATE
        data['area_5'] = oocytes[4].area * CONVERSION_RATE
        data['area_6'] = oocytes[5].area * CONVERSION_RATE
        data['area_7'] = oocytes[6].area * CONVERSION_RATE
        data['area_8'] = oocytes[7].area * CONVERSION_RATE
        data['area_9'] = oocytes[8].area * CONVERSION_RATE
        data['area_10'] = oocytes[9].area * CONVERSION_RATE
        data['year'] = datetime.datetime.now().year
        data['sample'] = self.sample_num
        payload = [data]
        client.upsert("km2u-hwjw", payload)


    #creates a new crab, finds all of its images and adds them to the system
    #also imports oocyte instances for each image
    #find path, for each folder, create crab, read its data from socrata, read all the images on that path
    @classmethod
    def create_image_instances(cls, path):
        print(path)
        for root, dirs, files in os.walk(path, topdown=False):
            for folder in dirs:
                sn = int(folder)
                #If the crab is not already in the system, then create it
                if(Crab.objects.filter(sample_num = sn).count() == 0):
                    client = Socrata("noaa-fisheries-afsc.data.socrata.com", "q3DhSQxvyWbtq1kLPs5q7jwQp",  username="cfitzgib@andrew.cmu.edu", password = "Kodiak18!")
                    crab_info = client.get("n49y-v5db", where=("sample = " + str(sn)))
                    lat, lon = crab_info[0]['location_1']['latitude'], crab_info[0]['location_1']['longitude']
                    yr, wt = crab_info[0]['year'], crab_info[0]['bottom_temp_c']
                    sc = crab_info[0]['shell_condition']
                    crab = Crab(sample_num=sn, year=yr, longitude=lon, latitude=lat, water_temp = wt, shell_condition = sc)
                
                
                    #This path would be where all the images are stored locally before upload
                    #Python script should be pushing images to this path along with its csv file
                    if(path[-1:] == '/'):
                        image_folder = path + str(sn)
                    else:
                        image_folder = path + '/' + str(sn)
                    crab.save()

                    for filename in os.listdir(image_folder):
                        #look for a resized image and then find its labeled counterpart
                        if(filename[-12:] == "_resized.png"):
                            #tag is the identifier for that image
                            tag = filename[:-12]
                            
                            #open both original and resized
                            orig = File(open(image_folder + '/' + tag + '_resized.png', 'rb'))
                            label = File(open(image_folder + '/' + tag + '_labeled.png', 'rb'))

                            data = tag + "_area.csv"

                            #create Image instance and save images to the media root directory
                            image = Image(crab=crab, csv = data)
                            image.original_img.save(tag + "_resize.png", orig, save=False)
                            image.binarized_img.save(tag + "_label.png", label, save=False)
                            image.save()

                            #read csv for image and import new oocyte instances
                            #csv must be located in the original path directory where the images were stored
                            with open(image_folder + '/' + data, 'r', newline='') as csvfile:
                                areareader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
                                for row in areareader:
                                    area, xcenter, ycenter = row[0], row[1], row[2]
                                    Oocyte.objects.create(crab=crab, image = image, area = area, center_x = xcenter, center_y = ycenter)

    def __str__(self):
        return ("crab (pk=" + str(self.id) + ", sample_num=" + str(self.sample_num) + ")")
        #return str((self.sample_num, self.done_oocytes, self.year, self.longitude, self.latitude, self.water_temp))

def get_upload_path(instance, filename):
    return '{0}/{1}'.format(instance.crab.sample_num, filename)

class Image(models.Model):
    crab = models.ForeignKey(Crab, on_delete = models.CASCADE) # when crab is deleted, images are deleted
    # path of the original and binarized image
    original_img = models.ImageField(upload_to=get_upload_path)
    binarized_img = models.ImageField(upload_to=get_upload_path)
    # string of the csv file name
    csv = models.CharField(max_length = 100)

    def get_img_num(self):
        # example file name: '63/untitled014_resize.png'
        file = self.original_img.name
        # example halfname: '014_resize.png'
        halfname = file.split("untitled")[1]
        # example num: 014
        num = halfname.split("_")[0]
        return num

    def __str__(self):
        return ("image (pk=" + str(self.id) + ")")

    #Given a click position, finds which of an image's
    #oocytes are closest and returns that oocyte
    def find_closest_oocyte(self, xclick, yclick):
        oocytes = Oocyte.objects.filter(image=self.id)
        pt = (float(xclick),float(yclick))
        min_dist = -1
        mindex = -1
        for idx, oocyte in enumerate(oocytes):
            oocyte_center = (oocyte.center_x, oocyte.center_y)
            dist = distance(pt, oocyte_center)
            if(dist < min_dist or min_dist == -1):
                min_dist = dist
                mindex = idx
        return oocytes[mindex]

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

class Oocyte(models.Model):
    crab = models.ForeignKey(Crab, on_delete = models.CASCADE)
    image = models.ForeignKey(Image, on_delete = models.CASCADE)
    chosen_count = models.IntegerField(default = 0) # how many times an oocyte has been clicked by others
    area = models.IntegerField()
    center_x = models.FloatField()
    center_y = models.FloatField()

    def __str__(self):
        return ("oocyte (pk=" + str(self.id) + ")")

    # method to increment chosen_count each time somebody clicks on a particular oocyte
    def increment_chosen_count(self):
        self.chosen_count+=1
        self.save()
        if(self.chosen_count == 10):
            self.crab.done_oocytes += 1
            self.crab.save()
            if(self.crab.done_oocytes >= 10):
                self.crab.send_crab_data()
    # method to call Crab model to increment done_oocyte once chosen_count reaches desired accuracy 

    # method to check if done_oocyte already incremented once for this instance of Oocyte, 
    # then increment chosen_count but not done_oocyte


class PlaySession(models.Model):
    num_photos = models.IntegerField(default = 8) # assume 12 photos per game session for now
    # photos = ArrayField(max_length = num_photos)
    completed_photos = models.IntegerField(default = 0)

    # method to end PlaySession when completed_photos is incremented to equal num_photos
    #global photos
    # method to increment completed_photos
    def __str__(self):
        return ("playSession (pk=" + str(self.id) + ")")

    # create a list of 12 photos with random images for user to play when PlaySession instance is created
    def setPhotos(self):
        allCrabs = list(Crab.objects.all())
        crabList = random.sample(allCrabs, 4) # pick 4 random crabs per PlaySession 
        
        photos = []
        for i in range (0, len(crabList)):
            images = list(crabList[i].image_set.all()) # look at all images from one crab of crabList
            playImg = random.sample(images, 2) # pick 3 random images from each crab
            for j in range (0, len(playImg)):
                photos.append(playImg[j])
                psi = PlaySessionImage(image = playImg[j], session = self)
                psi.save()
        return photos
    
    def getCrabs(self):
        analyzedCrabs = []
        sessionPhotos = PlaySessionImage.objects.filter(session = self)
        for i in range(0, len(sessionPhotos)):
            crab = sessionPhotos[i].image.crab
            analyzedCrabs.append(crab)
        return analyzedCrabs

class PlaySessionImage(models.Model):
    image = models.ForeignKey(Image, on_delete = models.CASCADE)
    session = models.ForeignKey(PlaySession, on_delete = models.CASCADE)

from django.dispatch import receiver

@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.original_img:
        if os.path.isfile(instance.original_img.path):
            os.remove(instance.original_img.path)
            os.remove(instance.binarized_img.path)

@receiver(models.signals.pre_save, sender=Image)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file1 = Image.objects.get(pk=instance.pk).original_img
        old_file2 = Image.objects.get(pk=instance.pk).binarized_img
    except Image.DoesNotExist:
        return False

    new_file1 = instance.original_img
    if not (old_file1 == new_file1):
        if os.path.isfile(old_file1.path):
            os.remove(old_file1.path)
            os.remove(old_file2.path)


