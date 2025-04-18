from django.db import models

class Dataset(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    # Relacionamento com outro dataset
    relacionado_a = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='datasets_relacionados', 
        verbose_name='Relacionado a'
    )
    
    def __str__(self):
        return self.nome

class Dado(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='dados')
    chave = models.CharField(max_length=100)
    valor = models.TextField(max_length=10000000, blank=True, null=True)
    id = models.AutoField(primary_key=True, unique=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    idade = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    sexo = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.chave}: {self.valor}"
