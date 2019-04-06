from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context = {}
    return render(request, 'gestionMachines/index.html', context)

def about(request):
    context = {}
    return render(request, 'gestionMachines/about.html', context)

def contact(request):
    context = {}
    return render(request, 'gestionMachines/contact.html', context)

def signin(request):
    context = {}
    return render(request, 'gestionMachines/signin.html', context)

def signup(request):
    context = {}
    return render(request, 'gestionMachines/signup.html', context)

def termsConditions(request):
    context = {}
    return render(request, 'gestionMachines/terms_conditions.html', context)