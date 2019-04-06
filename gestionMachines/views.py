from django.shortcuts import render
from django.http import HttpResponse

from .forms import CreateMODSOUserForm

# Page accueil
def index(request):
    context = {}
    return render(request, 'gestionMachines/index.html', context)

# A propose
def about(request):
    context = {}
    return render(request, 'gestionMachines/about.html', context)

# Contact
def contact(request):
    context = {}
    return render(request, 'gestionMachines/contact.html', context)

# Enregistrement d'utilisateur
def signin(request):
    context = {}
    return render(request, 'gestionMachines/signin.html', context)

# Connexion
def signup(request):
    form = CreateMODSOUserForm()
    context = {'form' : form}
    return render(request, 'gestionMachines/signup.html', context)

# Post enregistrement utilisateur
def signupResult(request):
    if request.method == 'POST':
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        parrain = request.POST.get('parrain')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        check_terms = request.POST.get('check_terms')
        
        success = True
        message = f"{prenom}, {nom}, {email}, {parrain}, {password}, {password_confirm}, {check_terms}"

    else:
        success = False
        message = "Une erreur serveur s'est produite. Pardon pour le dérangement."
    context = {
        'success' : success,
        'message' : message
    }
    return render(request, 'gestionMachines/signupResult.html', context)

# Termes et conditions
def termsConditions(request):
    context = {}
    return render(request, 'gestionMachines/terms_conditions.html', context)