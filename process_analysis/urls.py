from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProcessViewSet,
    UploadProcessPageView,
)

# Configurando o roteador para a API
router = DefaultRouter()
router.register("processes-api", ProcessViewSet, basename="processes-api")

urlpatterns = [
    # Endpoint para renderizar o template upload_process.html (frontend)
    path("upload/", UploadProcessPageView.as_view(), name="upload-process-page"),
    # Endpoints da API
    path("", include(router.urls)),  # Use apenas o roteador aqui
]
