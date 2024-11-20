from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProcessListAPI,
    ProcessDetailAPI,
    ProcessViewSet,
    upload_process,
    ProcessListPageView,
    UploadProcessPageView,
    ProcessDetailPageView,
)

# Configurando o roteador para a API
router = DefaultRouter()
router.register("processes", ProcessViewSet)

urlpatterns = [
    # Endpoint para o upload de um novo processo (frontend)
    path("upload/", UploadProcessPageView.as_view(), name="upload_process_page"),
    # Endpoint para a listagem de processos (frontend)
    path("processes/", ProcessListPageView.as_view(), name="process_list_page"),
    # Endpoint para os detalhes de um processo (frontend)
    path(
        "processes/<int:pk>/",
        ProcessDetailPageView.as_view(),
        name="process_detail_page",
    ),
    # API de processos
    path("api/upload/", upload_process, name="upload_process_api"),
    path("api/processes/", ProcessListAPI.as_view(), name="process_list_api"),
    path(
        "api/processes/<int:pk>/", ProcessDetailAPI.as_view(), name="process_detail_api"
    ),
    path("api/", include(router.urls)),
]
