from django.db import models

# Create your models here.
class Url(models.Model):
    shorturl = models.CharField(max_length=9, primary_key=True)
    originalurl = models.CharField(max_length=300)

