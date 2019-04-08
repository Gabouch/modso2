from django.db import models
from django.contrib.auth.models import User

class MODSOUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nomParrain = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    tel = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}, parrain {self.nomParrain}"