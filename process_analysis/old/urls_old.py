from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_process, name="upload_process"),
    path("", views.process_list, name="process_list"),
]
