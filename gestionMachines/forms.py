from django.forms import ModelForm, TextInput
from .models import MODSOUser

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