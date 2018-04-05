from django.db import models

# Create your models here.

class PlaySession(models.Model):
    num_photos = models.IntegerField(default = 5)
