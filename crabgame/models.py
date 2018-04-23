from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.core.files import File
import datetime
import random
import os
import csv
import re


# Create your models here.
class Crab(models.Model):
    sample_num = models.IntegerField(default = 0) # used to find the crab image
    # number of oocytes that reached more than 10 clicks
    done_oocytes = models.IntegerField(default = 0, validators = [MaxValueValidator(10)])
    year = models.IntegerField(default = datetime.date.today().year)
    longitude = models.FloatField()
    latitude = models.FloatField()
    water_temp = models.FloatField() 

    #creates a new crab, finds all of its images and adds them to the system
    #also imports oocyte instances for each image
    @classmethod
    def create_image_instances(cls, sn, yr, lon, lat, wt):
        crab = Crab(sample_num=sn, year=yr, longitude=lon, latitude=lat, water_temp = wt)
        
        #This path would be where all the images are stored locally before upload
        #Python script should be pushing images to this path along with its csv file
        path = 'D:/School/67-373 IS Consulting Project/crab_images/' + str(crab.sample_num)
        crab.save()

        #image = Image(crab.id, path + '/oocyte_resized.png', path + '/oocyte_labeled.png', path + '/oocyte_area.csv')
        for filename in os.listdir(path):
            #look for a resized image and then find its labeled counterpart
            if(filename[-12:] == "_resized.png"):
                #tag is the identifier for that image
                tag = filename[:-12]
                
                #open both original and resized
                orig = File(open(path + '/' + tag + '_resized.png', 'rb'))
                label = File(open(path + '/' + tag + '_labeled.png', 'rb'))

                data = tag + "_area.csv"

                #create Image instance and save images to the media root directory
                image = Image(crab=crab, csv = data)
                image.original_img.save(tag + "_resize.png", orig, save=False)
                image.binarized_img.save(tag + "_label.png", label, save=False)
                print(image.original_img)
                image.save()

                #read csv for image and import new oocyte instances
                #csv must be located in the original path directory where the images were stored
                with open(path + '/' + data, 'r', newline='') as csvfile:
                    areareader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
                    for row in areareader:
                        area, xcenter, ycenter = row[0], row[1], row[2]
                        Oocyte.objects.create(crab=crab, image = image, area = area, center_x = xcenter, center_y = ycenter)

    def __str__(self):
        return ("crab (pk=" + str(self.id) + ", sample_num=" + str(self.sample_num) + ")")
        #return str((self.sample_num, self.done_oocytes, self.year, self.longitude, self.latitude, self.water_temp))

    # method to increment the crab's done_oocyte once chosen_count reaches desired accuracy --> if conditional

    # method to stop displaying the crab to users once done_oocytes reaches 10 

    # if done_oocytes reaches 10, method to delete all instances of Oocytes that do not have chosen_count 10

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
        file = self.original_img.name
        img_num = file[10:13]
        return img_num

    def __str__(self):
        return ("image (pk=" + str(self.id) + ")")

class Oocyte(models.Model):
    crab = models.ForeignKey(Crab, on_delete = models.CASCADE)
    image = models.ForeignKey(Image, on_delete = models.CASCADE)
    chosen_count = models.IntegerField(default = 0) # how many times an oocyte has been clicked by others
    area = models.IntegerField()
    center_x = models.FloatField()
    center_y = models.FloatField()

    def __str__(self):
        return ("image (pk=" + str(self.id) + ")")
    # method to increment chosen_count each time somebody clicks on a particular oocyte

    # method to call Crab model to increment done_oocyte once chosen_count reaches desired accuracy 

    # method to check if done_oocyte already incremented once for this instance of Oocyte, 
    # then increment chosen_count but not done_oocyte


class PlaySession(models.Model):
    num_photos = models.IntegerField(default = 12) # assume 12 photos per game session for now
    #photos = models.ArrayField(max_length = num_photos)
    completed_photos = models.IntegerField(default = 0)

    # method to end PlaySession when completed_photos is incremented to equal num_photos

    # method to increment completed_photos
    def __str__(self):
        return ("image (pk=" + str(self.id) + ")")


    # create a list of 12 photos with random images for user to play when PlaySession instance is created
    def setPhotos(self):
        allCrabs = list(Crab.objects.all())
        crabList = random.sample(allCrabs, 4) # pick 4 random crabs per PlaySession 
        photos = []
        for i in range (0, len(crabList)):
            images = list(crabList[i].image_set.all()) # look at all images from one crab of crabList
            playImg = random.sample(images, 3) # pick 3 random images from each crab
            for j in range (0, len(playImg)):
                photos.append(playImg[j])
        return photos

class SchoolClass(models.Model):
    className = models.CharField(max_length = 100)

    def __str__(self):
        return ("image (pk=" + str(self.id) + ")")

class Intermediate(models.Model):
    oocyte = models.ForeignKey(Oocyte, on_delete = models.CASCADE)
    session = models.ForeignKey(PlaySession, on_delete = models.CASCADE) # need to fix later!!!!
    schoolClass = models.ForeignKey(SchoolClass, on_delete = models.CASCADE)

    def __str__(self):
        return ("image (pk=" + str(self.id) + ")")


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


