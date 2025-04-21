from rest_framework import viewsets, status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib import messages

from .models import Dataset, Dado
from .serializers import DatasetSerializer, DadoSerializer
from .forms import DatasetForm, CadastroForm

import csv
import json
from io import StringIO, TextIOWrapper

# ==========================
# ViewSets para API REST
# ==========================

class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

class DadoViewSet(viewsets.ModelViewSet):
    queryset = Dado.objects.all()
    serializer_class = DadoSerializer

# ==========================
# API REST manual
# ==========================

@api_view(['GET', 'POST'])
def dataset_list(request):
    if request.method == 'GET':
        datasets = Dataset.objects.all()
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DatasetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def dataset_detail(request, pk):
    try:
        dataset = Dataset.objects.get(pk=pk)
    except Dataset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DatasetSerializer(dataset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ==========================
# Importação de Arquivos
# ==========================

@login_required
@api_view(['POST'])
@parser_classes([MultiPartParser])
def importar_csv(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    arquivo = request.FILES.get('arquivo')
    if not arquivo.name.endswith('.csv'):
        return JsonResponse({'erro': 'O arquivo precisa ser CSV'}, status=400)

    decoded = arquivo.read().decode('utf-8')
    csv_reader = csv.DictReader(StringIO(decoded))
    dados_importados = 0

    for row in csv_reader:
        try:
            if all([row.get(campo) for campo in ['chave', 'valor', 'nome', 'idade', 'email', 'sexo']]):
                Dado.objects.create(
                    dataset=dataset,
                    chave=row['chave'],
                    valor=row['valor'],
                    nome=row['nome'],
                    idade=int(row['idade']),
                    email=row['email'],
                    sexo=row['sexo']
                )
                dados_importados += 1
        except Exception:
            continue

    return JsonResponse({'mensagem': f'Importação realizada com sucesso! {dados_importados} registros adicionados.'})

@login_required
@api_view(['POST'])
@parser_classes([MultiPartParser])
def importar_json(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    arquivo = request.FILES.get('arquivo')
    if not arquivo.name.endswith('.json'):
        return JsonResponse({'erro': 'O arquivo precisa ser JSON'}, status=400)

    decoded = arquivo.read().decode('utf-8')
    dados_json = json.loads(decoded)

    for item in dados_json:
        if all([item.get(campo) for campo in ['chave', 'valor', 'nome', 'idade', 'email', 'sexo']]):
            Dado.objects.create(
                dataset=dataset,
                chave=item['chave'],
                valor=item['valor'],
                nome=item['nome'],
                idade=item['idade'],
                email=item['email'],
                sexo=item['sexo']
            )

    return JsonResponse({'mensagem': 'Importação realizada com sucesso!'})

# ==========================
# Exportação de Arquivos
# ==========================

@api_view(['GET'])
def exportar_csv(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    dados = Dado.objects.filter(dataset=dataset)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{dataset.nome}.csv"'

    writer = csv.writer(response)
    writer.writerow(['chave', 'valor', 'id', 'nome', 'idade', 'email', 'sexo'])

    for dado in dados:
        writer.writerow([dado.chave, dado.valor, dado.id, dado.nome, dado.idade, dado.email, dado.sexo])

    return response

@api_view(['GET'])
def exportar_json(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    dados = Dado.objects.filter(dataset=dataset)
    lista = [
        {'chave': d.chave, 'valor': d.valor, 'id': d.id, 'nome': d.nome,
         'idade': d.idade, 'email': d.email, 'sexo': d.sexo}
        for d in dados
    ]
    return JsonResponse(lista, safe=False)

# ==========================
# Templates HTML (Autenticados)
# ==========================

#@login_required
def listar_datasets(request):
    datasets = Dataset.objects.all()
    return render(request, 'datasets/listar.html', {'datasets': datasets})

@login_required
def criar_dataset(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_datasets')
    else:
        form = DatasetForm()

    return render(request, 'datasets/criar.html', {'form': form})

@login_required
def upload_arquivo(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)

    if request.method == 'POST':
        arquivo = request.FILES.get('arquivo')
        if not arquivo:
            return render(request, 'datasets/upload.html', {'dataset': dataset, 'erro': 'Nenhum arquivo enviado.'})

        tipo = request.POST.get('tipo')
        if tipo == 'csv':
            reader = csv.DictReader(TextIOWrapper(arquivo.file, encoding='utf-8'))
            for row in reader:
                if all([row.get(campo) for campo in ['chave', 'valor', 'nome', 'idade', 'email', 'sexo']]):
                    Dado.objects.create(dataset=dataset, **row)

        elif tipo == 'json':
            dados = json.load(arquivo)
            for item in dados:
                if all([item.get(campo) for campo in ['chave', 'valor', 'nome', 'idade', 'email', 'sexo']]):
                    Dado.objects.create(dataset=dataset, **item)

        return redirect('listar_datasets')

    return render(request, 'datasets/upload.html', {'dataset': dataset})

# ==========================
# Visualização e CRUD dos Dados
# ==========================

def ver_dados(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    dados = Dado.objects.filter(dataset=dataset)
    return render(request, 'datasets/ver_dados.html', {'dataset': dataset, 'dados': dados})

@login_required
def adicionar_dado(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)

    if request.method == 'POST':
        campos = {k: request.POST.get(k) for k in ['chave', 'valor', 'nome', 'idade', 'email', 'sexo']}
        if all(campos.values()):
            Dado.objects.create(dataset=dataset, **campos)
            return redirect('ver_dados', pk=pk)

    return render(request, 'datasets/adicionar_dado.html', {'dataset': dataset})

@login_required
def editar_dado(request, pk):
    dado = get_object_or_404(Dado, pk=pk)

    if request.method == 'POST':
        for campo in ['chave', 'valor', 'nome', 'idade', 'email', 'sexo']:
            setattr(dado, campo, request.POST.get(campo))
        dado.save()
        return redirect('ver_dados', pk=dado.dataset.pk)

    return render(request, 'datasets/editar_dado.html', {'dado': dado})

@login_required
def remover_dado(request, pk):
    dado = get_object_or_404(Dado, pk=pk)
    dataset_id = dado.dataset.pk
    dado.delete()
    return redirect('ver_dados', pk=dataset_id)

# ==========================
# Exportações via Template
# ==========================

def exportar_csv_view(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    dados = dataset.dados.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{dataset.nome}.csv"'

    writer = csv.writer(response)
    writer.writerow(['chave', 'valor', 'id', 'nome', 'idade', 'email', 'sexo'])
    for dado in dados:
        writer.writerow([dado.chave, dado.valor, dado.id, dado.nome, dado.idade, dado.email, dado.sexo])

    return response

def exportar_json_view(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    dados = dataset.dados.all()
    data = [
        {'chave': d.chave, 'valor': d.valor, 'id': d.id, 'nome': d.nome,
         'idade': d.idade, 'email': d.email, 'sexo': d.sexo}
        for d in dados
    ]
    return HttpResponse(json.dumps(data, indent=2), content_type='application/json')

def logout_view(request):
    logout(request)
    return redirect('login')  

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça o login.')
            return redirect('login')
    else:
        form = CadastroForm()
    return render(request, 'cadastro.html', {'form': form})