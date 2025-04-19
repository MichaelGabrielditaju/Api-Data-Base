from django import forms
from .models import Dataset
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['nome']  # Aqui, você pode adicionar mais campos se o seu modelo tiver mais atributos.
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Dataset'}),
        }

class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']