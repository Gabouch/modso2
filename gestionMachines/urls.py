from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views

app_name="machines"

urlpatterns = [
    path('creermachine', login_required(views.CreerMachineView.as_view()), name='creermachine'),
    path('mesmachines', views.listerMachinesUtilisateur, name='mesmachines'),
    path('machines', views.listerMachines, name='machines'),
    path('machine/<int:pk>/', login_required(views.MachineView.as_view()), name='detail'),
    path('supprimermachine/<int:pk>', views.supprimerMachine, name='supprimermachine'),
    path('modifiermachine/<int:pk>', login_required(views.ModifierMachineView.as_view()), name='modifiermachine'),
]
