# Register your models here.
from django.contrib import admin
from .models import Dataset, Dado

class DatasetAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'criado_em', 'relacionado_a']
    search_fields = ['nome']
    list_filter = ['criado_em']


admin.site.register(Dataset)
admin.site.register(Dado)
