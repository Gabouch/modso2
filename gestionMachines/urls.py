from django.urls import path, include
from . import views

app_name="machines"

urlpatterns = [
    path('creermachine', views.creerMachine, name='creermachine'),
    path('mesmachines', views.ListerMachinesUtilisateur, name='mesmachine'),
    
]