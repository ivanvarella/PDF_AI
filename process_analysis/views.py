from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Process
from .serializers import ProcessSerializer
from rest_framework import viewsets


# ViewSet para listar e manipular Processos via API
class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer


# View para listar todos os Processos via API
class ProcessList(APIView):
    def get(self, request):
        processes = Process.objects.all()
        serializer = ProcessSerializer(processes, many=True)
        return Response(serializer.data)


# View para exibir os detalhes de um único Processo
class ProcessDetail(APIView):
    def get(self, request, pk):
        try:
            process = Process.objects.get(pk=pk)
        except Process.DoesNotExist:
            return Response(
                {"error": "Process not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProcessSerializer(process)
        return Response(serializer.data)


# Função para fazer upload de um novo processo via POST
@api_view(["POST"])
def upload_process(request):
    if request.method == "POST":
        data = request.data
        # Aqui você pode ajustar os campos conforme o modelo Process
        try:
            process = Process.objects.create(
                **data
            )  # Cria o processo com os dados recebidos
            return Response(
                {"message": "Process uploaded successfully", "process_id": process.id},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
