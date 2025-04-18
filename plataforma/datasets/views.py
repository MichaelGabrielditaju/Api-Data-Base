from rest_framework import viewsets, status
from .serializers import DatasetSerializer, DadoSerializer
import csv
import json
from io import StringIO, TextIOWrapper
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import Dataset, Dado
from django.shortcuts import get_object_or_404, render, redirect
from .forms import DatasetForm


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


class DadoViewSet(viewsets.ModelViewSet):
    queryset = Dado.objects.all()
    serializer_class = DadoSerializer


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
    print(f"Iniciando importação para dataset ID: {dataset.id}")

    for row in csv_reader:
        print(f"Lendo linha: {row}")
        try:
            chave = row.get('chave')
            valor = row.get('valor')
            nome = row.get('nome')
            idade = int(row.get('idade')) if row.get('idade') else 0
            email = row.get('email')
            sexo = row.get('sexo')

            if chave and valor and nome and idade and email and sexo:
                Dado.objects.create(
                    dataset=dataset,
                    chave=chave,
                    valor=valor,
                    nome=nome,
                    idade=idade,
                    email=email,
                    sexo=sexo
                )
                dados_importados += 1
        except Exception as e:
            continue  # ou logar erro
    print(f"Criando Dado com dataset: {dataset}")
    return JsonResponse({'mensagem': f'Importação realizada com sucesso! {dados_importados} registros adicionados.'})


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
        chave = item.get('chave')
        valor = item.get('valor')
        nome = item.get('nome')
        idade = item.get('idade')
        email = item.get('email')
        sexo = item.get('sexo')

        if chave and valor and nome and idade and email and sexo:
            Dado.objects.create(dataset=dataset, chave=chave, valor=valor,
                                nome=nome, idade=idade, email=email, sexo=sexo)

    return JsonResponse({'mensagem': 'Importação realizada com sucesso!'})


@api_view(['GET'])
def exportar_csv(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    dados = Dado.objects.filter(dataset=dataset)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{dataset.nome}.csv"'

    writer = csv.writer(response)
    writer.writerow(['chave', 'valor', 'id', 'nome', 'idade', 'email', 'sexo'])

    for dado in dados:
        writer.writerow([dado.chave, dado.valor, dado.id,
                        dado.nome, dado.idade, dado.email, dado.sexo])

    return response


@api_view(['GET'])
def exportar_json(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    dados = Dado.objects.filter(dataset=dataset)

    lista = [{'chave': dado.chave, 'valor': dado.valor, 'id': dado.id, 'nome': dado.nome,
              'idade': dado.idade, 'email': dado.email, 'sexo': dado.sexo} for dado in dados]
    return JsonResponse(lista, safe=False)


def listar_datasets(request):
    datasets = Dataset.objects.all()
    return render(request, 'datasets/listar.html', {'datasets': datasets})


def upload_arquivo(request, dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)

    if request.method == 'POST':
        arquivo = request.FILES.get('arquivo')
        if not arquivo:
            return render(request, 'datasets/upload.html', {'dataset': dataset, 'erro': 'Nenhum arquivo enviado.'})

        tipo = request.POST.get('tipo')
        if tipo == 'csv':
            reader = csv.DictReader(TextIOWrapper(
                arquivo.file, encoding='utf-8'))
            for row in reader:
                chave = row.get('chave')
                valor = row.get('valor')
                nome = row.get('nome')
                idade = row.get('idade')
                email = row.get('email')
                sexo = row.get('sexo')
                if chave and valor and nome and idade and email and sexo:
                    Dado.objects.create(dataset=dataset, chave=chave, valor=valor,
                                        nome=nome, idade=idade, email=email, sexo=sexo)

        elif tipo == 'json':
            dados = json.load(arquivo)
            for item in dados:
                chave = item.get('chave')
                valor = item.get('valor')
                nome = item.get('nome')
                idade = item.get('idade')
                email = item.get('email')
                sexo = item.get('sexo')
                if chave and valor and nome and idade and email and sexo:
                    Dado.objects.create(dataset=dataset, chave=chave, valor=valor,
                                        nome=nome, idade=idade, email=email, sexo=sexo)

        return redirect('listar_datasets')

    return render(request, 'datasets/upload.html', {'dataset': dataset})


def exportar_csv_view(request, dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)
    dados = dataset.dados.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{dataset.nome}.csv"'

    writer = csv.writer(response)
    writer.writerow(['chave', 'valor', 'id', 'nome', 'idade', 'email', 'sexo'])
    for dado in dados:
        writer.writerow([dado.chave, dado.valor, dado.id,
                        dado.nome, dado.idade, dado.email, dado.sexo])

    return response


def exportar_json_view(request, dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)
    dados = dataset.dados.all()
    data = [{'chave': d.chave, 'valor': d.valor, 'id': d.id, 'nome': d.nome,
             'idade': d.idade, 'email': d.email, 'sexo': d.sexo} for d in dados]
    return HttpResponse(json.dumps(data, indent=2), content_type='application/json')


def criar_dataset(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o dataset no banco de dados
            # Redireciona para a lista de datasets após criação
            return redirect('listar_datasets')
    else:
        form = DatasetForm()

    return render(request, 'datasets/criar.html', {'form': form})


def ver_dados(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    dados = Dado.objects.filter(dataset=dataset)

    return render(request, 'datasets/ver_dados.html', {
        'dataset': dataset,
        'dados': dados,
    })


def adicionar_dado(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)

    if request.method == 'POST':
        chave = request.POST.get('chave')
        valor = request.POST.get('valor')
        id = request.POST.get('id')
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        sexo = request.POST.get('sexo')

        if chave and valor and nome and idade and email and sexo:
            Dado.objects.create(dataset=dataset, chave=chave, valor=valor,
                                nome=nome, idade=idade, email=email, sexo=sexo)
            return redirect('ver_dados', pk=pk)

    return render(request, 'datasets/adicionar_dado.html', {
        'dataset': dataset
    })


def editar_dado(request, pk):
    dado = get_object_or_404(Dado, pk=pk)

    if request.method == 'POST':
        dado.chave = request.POST.get('chave')
        dado.valor = request.POST.get('valor')
        dado.nome = request.POST.get('nome')
        dado.idade = request.POST.get('idade')
        dado.email = request.POST.get('email')
        dado.sexo = request.POST.get('sexo')
        dado.save()
        return redirect('ver_dados', pk=dado.dataset.pk)

    return render(request, 'datasets/editar_dado.html', {'dado': dado})


def remover_dado(request, pk):
    dado = get_object_or_404(Dado, pk=pk)
    dataset_id = dado.dataset.pk
    dado.delete()
    return redirect('ver_dados', pk=dataset_id)


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
