from django.contrib import admin
from django.urls import path, include
from datasets import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin
from django.contrib.auth import views as auth_views
from datasets import views

schema_view = get_schema_view(
    openapi.Info(
        title="API da Plataforma de Datasets",
        default_version='v1',
        description="Documentação da API com suporte a Postman e Insomnia.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('datasets.urls')), 
    path('', views.listar_datasets, name='listar_datasets'),
    path('upload/<int:dataset_id>/', views.upload_arquivo, name='upload_arquivo'),
    path('exportar-csv/<int:dataset_id>/', views.exportar_csv_view, name='exportar_csv_view'),
    path('exportar-json/<int:dataset_id>/', views.exportar_json_view, name='exportar_json_view'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ROTAS DO SWAGGER E REDOC
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
]

