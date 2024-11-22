from rest_framework import serializers
from .models import Process
from django.core.files.storage import default_storage
from rest_framework.exceptions import ValidationError
import uuid
import json


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = "__all__"

    # # Caso o JSONField precise de uma validação extra, você pode adicionar isso aqui.
    # def validate_partes(self, value):
    #     # Validar se 'partes' é uma lista válida
    #     try:
    #         # Se o valor não for um JSON válido, lançar erro
    #         value = json.loads(value)
    #     except ValueError:
    #         raise ValidationError("O campo 'partes' precisa ser um JSON válido.")
    #     return value

    # def validate_demandas(self, value):
    #     # Validar se 'demandas' é uma lista válida
    #     try:
    #         value = json.loads(value)
    #     except ValueError:
    #         raise ValidationError("O campo 'demandas' precisa ser um JSON válido.")
    #     return value


class ProcessUploadSerializer(serializers.ModelSerializer):
    arquivo = serializers.FileField()

    class Meta:
        model = Process
        fields = ["arquivo"]  # Aqui tratamos apenas o arquivo

    def validate_arquivo(self, value):
        """
        Valida a extensão do arquivo.
        """
        valid_extensions = ["pdf", "doc", "docx"]
        extension = value.name.split(".")[-1].lower()
        if extension not in valid_extensions:
            raise ValidationError("Arquivo deve ser um PDF, DOC ou DOCX.")
        return value

    def save(self, **kwargs):
        """
        Salva o arquivo usando o default_storage e retorna o caminho salvo.
        """
        arquivo = self.validated_data.get("arquivo")

        # Criar um nome único para o arquivo
        nome_arquivo = f"{uuid.uuid4()}_{arquivo.name}"
        file_path = f"pdfs/{nome_arquivo}"

        # Salvar o arquivo no sistema de arquivos utilizando o default_storage
        with default_storage.open(file_path, "wb+") as destination:
            for chunk in arquivo.chunks():
                destination.write(chunk)

        # Retornar o caminho do arquivo para ser usado na criação do processo
        return {"arquivo": file_path}
