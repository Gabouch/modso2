from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from collections import Counter
from django.db import transaction, IntegrityError

from .models import MODSOUser

# Page accueil
def index(request):
    return render(request, 'gestionMachines/index.html')

# A propose
def about(request):
    return render(request, 'gestionMachines/about.html')

# Contact
def contact(request):
    return render(request, 'gestionMachines/contact.html')

# Termes et conditions
def termsConditions(request):
    return render(request, 'gestionMachines/terms_conditions.html')

# Connexion
def signin(request):
    errors = []
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).first() is not None:
            userAuth = authenticate(request, username = email, password = password)
            if userAuth is not None:
                login(request, userAuth)
                return redirect('index')
            else:
                errors.append(f"Votre mot de passe est incorrect. Merci de réessayer.")
        else:
            errors.append(f"Aucun compte n'existe pour cette adresse mail. Merci de créer un compte.")
    context = {
        'errors' : errors
    }
    return render(request, 'gestionMachines/signin.html', context)

# Enregistrement de l'utilisateur
def signup(request):
    context = {}
    errors = []
    # Recup des info du formulaire
    if request.method == 'POST':
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        parrain = request.POST.get('parrain')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        check_terms = request.POST.get('check_terms')

        if not prenom:
            errors.append("Le prénom est obligatoire")
        if not nom:
            errors.append("Le nom est obligatoire")
        if not email:
            errors.append("L'email est obligatoire")
        if not parrain:
            errors.append("Le nom du parrain est obligatoire")
        if not password or not password_confirm:
            errors.append("Le mot de passe est obligatoire")
        if not (password) == (password_confirm):
            errors.append("Le mot de passe n'est pas cohérent")
        if not check_terms:
            errors.append("Merci de lire et accepter les conditions d'utilisation.")
        
        if not errors:
            #validation du parrain
            if User.objects.filter(last_name__icontains=parrain).first() is not None :
                # validation utilisateur n'existe pas deja
                if User.objects.filter(email=email).first() is None:
                    try:
                        user = None
                        with transaction.atomic():
                            # creation user
                            user = User.objects.create(first_name=prenom, last_name=nom, email=email, username=email)
                            # creation MODSOUser
                            MODSOUser.objects.create(user=user, nomParrain=parrain)
                            # Enregistrement du mot de passe
                            user.set_password(password)
                            user.save()
                        # Auth de l'utilisateur
                        userAuth = authenticate(request, username=email, password=password)
                        # login de l'utilisateur
                        if userAuth is not None:
                            login(request, userAuth)
                            return redirect('signupResult')
                        else:
                            raise Exception(f"erreur lors de l'authentification de l'utilisateur {user.username} / {user.password}.")
                    except IntegrityError:
                        errors.append("Une erreur serveur est survenue lors de l'enrgistrement en base. Merci de contacter le service technique.")
                    except Exception as e:
                        errors.append(f"Une erreur serveur est survenue {e.args}  Merci de prévenir le service technique.")
                else:
                    errors.append("Cette adresse mail est déjà utilisée.")
            else:
                errors.append("Le parrain n'existe pas. Merci de renseigner un parrain déjà inscrit ou de contacter le support technique.")
    else:
        pass
    
    context = {
        'errors' : errors
    }
    return render(request, 'gestionMachines/signup.html', context)

# Post enregistrement utilisateur
@login_required
def signupResult(request):
    return render(request, 'gestionMachines/signupResult.html')

# Deconnexion
@login_required
def signout(request):
    logout(request)
    return render(request, 'gestionMachines/signout.html')
