from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

from .views import (
    DatasetViewSet, DadoViewSet,
    importar_csv, importar_json,
    exportar_csv, exportar_json,
    listar_datasets, upload_arquivo, exportar_csv_view, exportar_json_view
)

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet)
router.register(r'dados', DadoViewSet)

urlpatterns = [
    # API REST
    path('api/', include(router.urls)),
    path('api/datasets/<int:dataset_id>/importar-csv/', importar_csv),
    path('api/datasets/<int:dataset_id>/importar-json/', importar_json),
    path('api/datasets/<int:dataset_id>/exportar-csv/', exportar_csv),
    path('api/datasets/<int:dataset_id>/exportar-json/', exportar_json),

    # Interface via Django Template
    path('', listar_datasets, name='listar_datasets'),
    path('<int:dataset_id>/upload/', upload_arquivo, name='upload_arquivo'),
    path('<int:dataset_id>/exportar-csv/', exportar_csv_view, name='exportar_csv'),
    path('<int:dataset_id>/exportar-json/', exportar_json_view, name='exportar_json'),

    path('criar/', views.criar_dataset, name='criar_dataset'), 
    path('', include(router.urls)),

    path('<int:pk>/dados/', views.ver_dados, name='ver_dados'),
    path('<int:pk>/dados/adicionar/', views.adicionar_dado, name='adicionar_dado'),
    path('<int:pk>/editar_dado/', views.editar_dado, name='editar_dado'),
    path('<int:pk>/remover_dado/', views.remover_dado, name='remover_dado'),

]

