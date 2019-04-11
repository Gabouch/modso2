"""modso2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from gestionMachines import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='gestionMachines/index.html'), name='index'),
    path('about', TemplateView.as_view(template_name='gestionMachines/about.html'), name='about'), 
    path('contact', TemplateView.as_view(template_name='gestionMachines/contact.html'), name='contact'), 
    path('terms_conditions', TemplateView.as_view(template_name='gestionMachines/terms_conditions.html'), name='terms_conditions'), 
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signupResult', views.signupResult, name='signupResult'),
    path('espaceperso', views.espacePerso, name='espaceperso'),
    path('espaceperso/infoconnexion', views.espacePersoConnexion, name='espacepersoconnexion'),
    path('espaceperso/infoperso', views.espacePersoPerso, name='espacepersoperso'),
    path('espaceperso/suppression', views.suppressioncompte, name='suppressioncompte'),
    path('signout', views.signout, name='signout'),
    path('machines/', include('gestionMachines.urls', namespace='machines')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
