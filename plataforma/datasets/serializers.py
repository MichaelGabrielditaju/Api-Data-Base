from rest_framework import serializers
from .models import Dataset, Dado

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'nome', 'descricao', 'criado_em', 'relacionado_a', 'datasets_relacionados']

class DadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dado
        fields = ['id', 'chave', 'valor', 'nome', 'idade', 'email', 'sexo', 'dataset']