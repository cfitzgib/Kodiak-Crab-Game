from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import datetime

# Create your models here.
class Crab(models.Model):
    done_oocytes = models.IntegerField(default = 0, validators = [MaxValueValidator(10)])
    year = models.IntegerField(default = datetime.date.today().year)
    longitude = models.FloatField()
    latitude = models.FloatField()
    water_temp = models.FloatField() 

    def __str__(self):
        return str((self.done_oocytes, self.year, self.longitude, self.latitude, self.water_temp))

    # method to increment the crab's done_oocyte once chosen_count reaches desired accuracy --> if conditional

    # method to stop displaying the crab to users once done_oocytes reaches 10 

    # if done_oocytes reaches 10, method to delete all instances of Oocytes that do not have chosen_count 10

class Image(models.Model):
    crab = models.ForeignKey(Crab, on_delete = models.CASCADE) # when crab is deleted, images are deleted
    original_img = models.ImageField(upload_to='uploads/crab.id', height_field=486, width_field=648) 
    binarized_img = models.ImageField(upload_to='uploads/crab.id', height_field=486, width_field=648)
    csv = models.CharField(max_length = 100)

class Oocyte(models.Model):
    crab = models.ForeignKey(Crab, on_delete = models.CASCADE)
    image = models.ForeignKey(Image, on_delete = models.CASCADE)
    chosen_count = models.IntegerField(default = 0) # how many times an oocyte has been clicked by others
    area = models.IntegerField()
    center_x = models.FloatField()
    center_y = models.FloatField()

    # method to increment chosen_count each time somebody clicks on a particular oocyte

    # method to call Crab model to increment done_oocyte once chosen_count reaches desired accuracy 

    # method to check if done_oocyte already incremented once for this instance of Oocyte, 
    # then increment chosen_count but not done_oocyte


class PlaySession(models.Model):
    num_photos = models.IntegerField(default = 10) # assume 10 photos per game session for now
    completed_photos = models.IntegerField(default = 0)

    # method to end PlaySession when completed_photos is incremented to equal num_photos

    # method to increment completed_photos 

class SchoolClass(models.Model):
    className = models.CharField(max_length = 100)

class Intermediate(models.Model):
    oocyte = models.ForeignKey(Oocyte, on_delete = models.CASCADE)
    session = models.ForeignKey(PlaySession, on_delete = models.CASCADE) # need to fix later!!!!
    schoolClass = models.ForeignKey(SchoolClass, on_delete = models.CASCADE)


