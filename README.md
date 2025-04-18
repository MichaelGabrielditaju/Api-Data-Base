
# 📊 Api-Data-Base

Plataforma desenvolvida com Django e Django REST Framework para o gerenciamento completo de conjuntos de dados (datasets). Permite a criação, edição, exclusão, relacionamento entre datasets e a importação/exportação de arquivos nos formatos JSON e CSV.

## 🚀 Funcionalidades

- 📁 CRUD completo de datasets
- 🔄 Importação e exportação de datasets em JSON e CSV
- 🔗 Relacionamentos entre datasets
- 📘 Documentação interativa com Swagger e Redoc
- ✅ Compatível com Postman e Insomnia para testes de API

## 🛠️ Tecnologias Utilizadas

- [Python 3.12](https://www.python.org/)
- [Django 5.2](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/) (geração de documentação Swagger/Redoc)

## 📦 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/MichaelGabrielditaju/Api-Data-Base.git
cd Api-Data-Base
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # macOS/Linux
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Aplique as migrações do banco de dados:

```bash
python manage.py migrate
```

5. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

## 📘 Documentação da API

Acesse os endpoints da documentação interativa da API:

- Swagger UI: [`http://localhost:8000/swagger/`](http://localhost:8000/swagger/)
- Redoc: [`http://localhost:8000/redoc/`](http://localhost:8000/redoc/)

## 🧪 Testando com Postman ou Insomnia

- Todas as rotas estão documentadas em Swagger e Redoc.
- A API está pronta para testes com ferramentas como Postman e Insomnia.
- Basta importar a coleção ou testar diretamente com as URLs fornecidas na documentação.

## 📂 Estrutura básica do projeto

```
Api-Data-Base/
├── datasets/         # App principal com as views, serializers e urls
├── plataforma/       # Configurações do projeto Django
├── templates/        # Templates para Swagger e Redoc (opcional)
├── db.sqlite3        # Banco de dados padrão SQLite
├── manage.py
├── requirements.txt
└── README.md
``` 
---

Desenvolvido com 💻 por Michael Gabriel — [GitHub](https://github.com/MichaelGabrielditaju)
