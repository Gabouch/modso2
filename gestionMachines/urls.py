from django.urls import path, include
from . import views

app_name="machines"

urlpatterns = [
    path('creermachine', views.creerMachine, name='creermachine'),
    path('mesmachines', views.listerMachinesUtilisateur, name='mesmachines'),
    path('machines', views.listerMachines, name='machines'),
    path('machine/<int:pk>/', views.MachineView.as_view(), name='detail'),
]