from django.forms import ModelForm, TextInput, Textarea
from .models import MODSOUser, Machine

class MODSOUserForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MODSOUserForm, self).__init__(*args, **kwargs)
        self.fields['adresse'].required = False
        self.fields['tel'].required = False
    
    class Meta:
        model = MODSOUser
        fields = ['adresse', 'tel']
        widgets = {
            'adresse': TextInput(attrs={'class': 'form-control'}),
            'tel': TextInput(attrs={'class': 'form-control'}),
        }

class CreerMachineForm(ModelForm):

    class Meta:
        model = Machine
        fields = ['nom', 'description']
        widgets = {
            'nom' : TextInput(attrs={'class': 'form-control'}),
            'description' : Textarea(attrs={'class': 'form-control'}),
        }
