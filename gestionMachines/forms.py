from django.forms import ModelForm, TextInput, EmailInput, PasswordInput

from .models import MODSOUser


class CreateMODSOUserForm(ModelForm):
    model = MODSOUser
    fields = ['first_name', 'last_name', 'email', 'nomParrain', 'password']
    widget = {
        'first_name':TextInput(attrs = {'class' : 'form-control'}),
        'last_name':TextInput(attrs = {'class' : 'form-control'}),
        'email':EmailInput(attrs = {'class' : 'form-control'}),
        'nomParrain':TextInput(attrs = {'class' : 'form-control'}),
        'password': PasswordInput()),
    }