from django.db import models

# Create your models here.

class Marker(models.Model):
    address = models.TextField(max_length=200)
    mapID = models.TextField(max_length=200)
    user = models.TextField(max_length=200)