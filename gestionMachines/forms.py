from django.forms import ModelForm, TextInput, Textarea, ImageField, CharField, Form
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
        fields = ['nom', 'description', 'photo']
        widgets = {
            'nom' : TextInput(attrs={'class': 'form-control'}),
            'description' : Textarea(attrs={'class': 'form-control'}),
        }

class ModifierMachineForm(ModelForm):
    class Meta:
        model = Machine
        fields = ['nom', 'description', 'photo']
        widgets = {
            'nom' : TextInput(attrs={'class': 'form-control'}),
            'description' : Textarea(attrs={'class': 'form-control'}),
        }

class ChercherMachineForm(Form):
    nom_machine = CharField(label='Rechercher une machine', max_length=100)
    def __init__(self, *args, **kwargs):
        super(ChercherMachineForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'