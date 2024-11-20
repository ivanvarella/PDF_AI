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
from rest_framework.decorators import action


# ViewSet para listar e manipular Processos via API
class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    parser_classes = [
        MultiPartParser,
        FormParser,
    ]  # Permite trabalhar com arquivos e dados JSON

    def create(self, request, *args, **kwargs):
        # Extrair o arquivo do request
        file = request.FILES.get("file")

        if file:
            # Valida e processa o arquivo usando ProcessUploadSerializer
            file_data = {"file": file}
            upload_serializer = ProcessUploadSerializer(data=file_data)

            if not upload_serializer.is_valid():
                return Response(
                    upload_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            # O arquivo é válido, segue para validação dos outros dados
            validated_file = upload_serializer.validated_data.get("file")
        else:
            return Response(
                {"error": "Arquivo não fornecido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validação dos outros dados usando ProcessSerializer
        data = request.data.copy()
        data["arquivo"] = validated_file  # Inclui o arquivo validado

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def upload_process(self, request):
        """
        Endpoint dedicado, se necessário, que utiliza o mesmo fluxo do método `create`.
        """
        return self.create(request)


# View para listar todos os Processos via API
class ProcessListAPI(APIView):
    def get(self, request):
        processes = Process.objects.all()
        serializer = ProcessSerializer(processes, many=True)
        return Response(serializer.data)


# View para exibir os detalhes de um único Processo via API
class ProcessDetailAPI(APIView):
    def get(self, request, pk):
        try:
            process = Process.objects.get(pk=pk)
        except Process.DoesNotExist:
            return Response(
                {"error": "Process not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProcessSerializer(process)
        return Response(serializer.data)


# Função para fazer upload de um novo processo via POST (API)
@api_view(["POST"])
def upload_process(request):
    if request.method == "POST":
        print(f"request.data: {request.data}")
        # Acessando o arquivo diretamente
        # Acessando o arquivo diretamente
        uploaded_file = request.data.get("file")  # Retorna o InMemoryUploadedFile
        # if uploaded_file:
        #     print(f"File: {uploaded_file}")  # Imprime o objeto InMemoryUploadedFile
        #     print(f"File name: {uploaded_file.name}")  # Nome do arquivo
        #     print(f"File content type: {uploaded_file.content_type}")  # Tipo MIME
        #     print(f"File size: {uploaded_file.size}")  # Tamanho do arquivo

        serializer = ProcessUploadSerializer(data=uploaded_file)

        if serializer.is_valid():
            # Salvar o novo processo
            process = serializer.save()
            return Response(
                {"message": "Process uploaded successfully", "process_id": process.id},
                status=status.HTTP_201_CREATED,
            )
        else:
            # Se o serializer não for válido, retorna o erro
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View para renderizar a página de upload de processo (Frontend)
class UploadProcessPageView(TemplateView):
    template_name = "upload_process.html"  # O template de upload


# View para renderizar a lista de processos (Frontend)
class ProcessListPageView(TemplateView):
    template_name = "process_list.html"  # O template da lista de processos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        processes = Process.objects.all()
        context["processes"] = processes
        return context


# View para renderizar os detalhes de um único processo (Frontend)
class ProcessDetailPageView(TemplateView):
    template_name = "process_detail.html"  # O template de detalhes do processo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]  # Obtém o 'pk' do processo a partir da URL
        try:
            process = Process.objects.get(pk=pk)
            context["process"] = process
        except Process.DoesNotExist:
            context["error"] = "Process not found"
        return context
