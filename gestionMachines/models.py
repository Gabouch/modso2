from django.db import models
from django.contrib.auth.models import User

class MODSOUser(User):
    nomParrain = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    tel = models.CharField(max_length=200)
