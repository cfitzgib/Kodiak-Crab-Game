from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Crab(models.Model):
    done_oocytes = models.IntegerField(validators = [MaxValueValidator(10)])

class Images(models.Model):
    crab = models.ForeignKey(Crab, on_delete = models.CASCADE) # when crab is deleted, images are deleted

class Oocytes(models.Model):
    crab = models.ForeignKey(Crab, on_delete = models.CASCADE)
    image = models.ForeignKey(Images, on_delete = models.CASCADE)

class OocyteMeasurement(models.Model):
    oocyte = models.ForeignKey(Oocytes, on_delete = models.CASCADE)
    session = models.ForeignKey(PlaySession, on_delete = PROTECT)
    schoolClass = models.ForeignKey(schoolClass, on_delete = PROTECT)
    area = models.IntegerField(default = 0)

class PlaySession(models.Model):
    num_photos = models.IntegerField(default = 5) # assume 5 photos per game session for now

class schoolClass(models.Model):
    className = models.CharField(max_length = 100)
