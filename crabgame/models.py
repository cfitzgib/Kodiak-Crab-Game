from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Crab(models.Model):
    done_oocytes = models.IntegerField(validators = [MaxValueValidator(10)])

class Images(models.Model):
    crab = models.ForeignKey(Crab, on_delete = models.CASCADE)

class Oocytes(models.Model):
    crab = models.ForeignKey(Crab, on_delete = models.CASCADE)
    image = models.ForeignKey(Images, on_delete = models.CASCADE)

class PlaySession(models.Model):
    num_photos = models.IntegerField(default = 5) # assume 5 photos per game session for now
