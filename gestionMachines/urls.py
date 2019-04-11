from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views

app_name="machines"

urlpatterns = [
    path('creermachine', login_required(views.CreerMachineView.as_view()), name='creermachine'),
    path('mesmachines', views.listerMachinesUtilisateur, name='mesmachines'),
    path('machines', views.listerMachines, name='machines'),
    path('machine/<int:pk>/', views.MachineView.as_view(), name='detail'),
]