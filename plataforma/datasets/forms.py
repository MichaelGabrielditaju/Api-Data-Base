from django import forms
from .models import Dataset

class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['nome']  # Aqui, você pode adicionar mais campos se o seu modelo tiver mais atributos.
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Dataset'}),
        }
