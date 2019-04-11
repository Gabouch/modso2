from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from collections import Counter
from django.db import transaction, IntegrityError
from django.core.validators import validate_email, ValidationError
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import MODSOUser, Machine
from .forms import MODSOUserForm, CreerMachineForm

ERREUR_SERVEUR = "Une erreur est survenu durant l'enregistrement de vos informations en base de donnée. Veuillez réessayer. Si l'erreur persiste, merci de contacter le support technique."

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
        try:
            validate_email(email)
        except ValidationError:
            errors.append("L'email est invalide.")
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
                        errors.append(f"Une erreur serveur est survenue {str(e)}  Merci de prévenir le service technique.")
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

# Espace utilisateur
def espacePerso(request):
    return render(request, 'gestionMachines/espaceperso/espaceperso.html')

# Modification des infos de connexion
@login_required
def espacePersoConnexion(request):
    if request.method == 'POST':
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        user = User.objects.filter(email=request.user.email).first()
        if user:
            try:
                with transaction.atomic():
                    # prenom
                    if prenom:
                        user.first_name=prenom
                        messages.add_message(request, messages.SUCCESS, "Le prénom a été modifié!")
                    # nom
                    if nom:
                        user.last_name=nom
                        messages.add_message(request, messages.SUCCESS, "Le nom a été modifié!")
                    # email
                    if email:
                        user.email=email
                        user.username=email
                        messages.add_message(request, messages.SUCCESS, "L'email a été modifié!")
                    # password
                    if password:
                        if password == password_confirm:
                            user.set_password(password)
                            messages.add_message(request, messages.SUCCESS, "Le mot de passe a été modifié!")
                        else:
                            messages.add_message(request, messages.ERROR, "Les mots de passe ne sont pas identiques. Le mot de passe n'a pas été modifié.")
                    user.save()
            except IntegrityError as e:
                messages.add_message(request, messages.ERROR, ERREUR_SERVEUR + f"Erreur : {str(e)}")
        return redirect('espaceperso')
    return render(request, 'gestionMachines/espaceperso/espaceperso_connexion.html')

# Modification des infos perso
@login_required
def espacePersoPerso(request):
    if request.method == 'POST':
        form = MODSOUserForm(request.POST)
        if form.is_valid():
            adresse = form.cleaned_data['adresse']
            tel = form.cleaned_data['tel']
            try:
                user = MODSOUser.objects.filter(user__email=request.user.email).first()
                if user:
                    with transaction.atomic():
                        if adresse:
                            user.adresse = adresse
                            messages.add_message(request, messages.SUCCESS, "L'adresse a été modifiée!")
                        if tel:
                            user.tel = tel
                            messages.add_message(request, messages.SUCCESS, "Le numéro de téléphone a été modifié!")
                        user.save()
                        print(user.adresse)
                        print(user.tel)
            except IntegrityError:
                messages.add_message(request, messages.ERROR, ERREUR_SERVEUR)
        else:
            messages.add_message(request, messages.ERROR, form.errors.items())
        return redirect('espaceperso')
    else:
        form = MODSOUserForm()
    return render(request, 'gestionMachines/espaceperso/espaceperso_perso.html', {'form' : form})

# Suppression du compte
@login_required
def suppressioncompte(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                user = User.objects.get(username=request.user.username)
                logout(request)
                user.delete()
        except IntegrityError:
            messages.add_message(request, messages.ERROR, ERREUR_SERVEUR)
        return redirect('index')

    return render(request, 'gestionMachines/espaceperso/espaceperso_suppression.html')

# Creation d'une nouvelle machine
# @login_required
# def creerMachine(request):
#     if request.method == 'POST':
#         form = CreerMachineForm(request.POST)
#         if form.is_valid():
#             nom = form.cleaned_data['nom']
#             description = form.cleaned_data['description']
#             try:
#                 with transaction.atomic():
#                     Machine.objects.create(user=request.user, nom=nom, description=description)
#                     messages.add_message(request, messages.SUCCESS, f"La machine {nom} a bien été crée")
#                     return redirect('machines:mesmachines')
#             except IntegrityError as e:
#                 messages.add_message(request, messages.ERROR, ERREUR_SERVEUR + f"Erreur : {str(e)}")
#         else:
#             messages.add_message(request, messages.ERROR, "Le formulaire n'est pas valide.")
#     else:
#         form = CreerMachineForm()
#     context = {'form' : form}
#     return render(request, 'gestionMachines/machines/creermachine.html', context)

 # Lister les machines de l'utilisateur connecté   
@login_required
def listerMachinesUtilisateur(request):
    machines = Machine.objects.filter(user=request.user)
    context = {'machines' : machines}
    return render(request, 'gestionMachines/machines/mesmachines.html', context)

# Lister toutes les machines
@login_required
def listerMachines(request):
    machines = Machine.objects.all()
    context = {'machines' : machines}
    return render(request, 'gestionMachines/machines/listemachines.html', context)

class MachineView(DetailView):
    model = Machine
    template_name='gestionMachines/machines/detail.html'

# Creation de vue de creation de machine
class CreerMachineView(CreateView):
    form_class = CreerMachineForm
    template_name='gestionMachines/machines/creermachine.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)