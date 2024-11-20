from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProcessList, ProcessDetail, ProcessViewSet, upload_process

router = DefaultRouter()
router.register("processes", ProcessViewSet)

urlpatterns = [
    path(
        "upload/", upload_process, name="upload_process"
    ),  # A função 'upload_process' é importada
    path(
        "", ProcessList.as_view(), name="process_list"
    ),  # Alterado de views.process_list para ProcessList.as_view()
    path("api/processes/", ProcessList.as_view(), name="process_list_api"),
    path("api/processes/<int:pk>/", ProcessDetail.as_view(), name="process_detail_api"),
    path("api/", include(router.urls)),  # Inclui as rotas da API
]
