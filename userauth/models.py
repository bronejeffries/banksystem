from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Defaultpasswords(models.Model):
    password = models.CharField(max_length=25, null = False )
