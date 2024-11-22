from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Process
from .serializers import ProcessSerializer, ProcessUploadSerializer
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser


# ViewSet API para o endpoint: http://127.0.0.1:8000/api/processes-api/
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Process
from .serializers import ProcessSerializer, ProcessUploadSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class ProcessViewSet(viewsets.ModelViewSet):
    """
    ViewSet que lida com Processos, permitindo métodos padrão do ModelViewSet.
    """

    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    parser_classes = [MultiPartParser, FormParser]  # Permite uploads de arquivos

    def create(self, request, *args, **kwargs):
        """
        Substitui o método POST padrão para incluir lógica de upload com ProcessUploadSerializer.
        """
        # Inicializa os dois serializers, um para o arquivo e outro para os outros dados
        upload_serializer = ProcessUploadSerializer(data=request.data)
        data_serializer = ProcessSerializer(data=request.data)

        # Validar o serializer para o arquivo
        if not upload_serializer.is_valid():
            return Response(
                upload_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        # Validar o serializer para os outros dados
        if not data_serializer.is_valid():
            return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Salvar o arquivo usando o ProcessUploadSerializer
        file_path = upload_serializer.save()

        # Criar um dicionário com os dados do processo, incluindo o arquivo salvo
        process_data = data_serializer.validated_data
        process_data["arquivo"] = file_path["arquivo"]

        # Salvar o processo completo no banco de dados
        process = Process.objects.create(**process_data)

        return Response(ProcessSerializer(process).data, status=status.HTTP_201_CREATED)


# View para renderizar a página de upload de processo (Frontend)
class UploadProcessPageView(TemplateView):
    template_name = "upload_process.html"  # O template de upload
