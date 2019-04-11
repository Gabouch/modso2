from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class MODSOUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nomParrain = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    tel = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}, parrain {self.nomParrain}"

class Machine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proprietaire')
    nom =  models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    disponible = models.BooleanField(default=True)
    utilisateur_actuel = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='utilisateur', null=True)
    photo = models.ImageField(upload_to='machines', null = True)

    def __str__(self):
        return f"{self.nom}"

    def get_absolute_url(self):
        return reverse('machines:detail', kwargs={'pk':self.pk})
