from django import forms
from .models import Dataset
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['nome', 'descricao', 'relacionado_a']  
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nome do Dataset'}), 
            'descricao': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Descrição do Dataset'}),  
            'relacionado_a': forms.Select(attrs={'class': 'form-select'})  
        }
class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']