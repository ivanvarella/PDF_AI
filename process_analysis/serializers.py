from rest_framework import serializers
from .models import Process
from django.core.files.storage import default_storage
from rest_framework.exceptions import ValidationError
import os
import uuid


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = "__all__"


class ProcessUploadSerializer(serializers.ModelSerializer):
    arquivo = serializers.FileField()

    class Meta:
        model = Process
        fields = "__all__"

    def validate_arquivo(self, value):
        # Validar a extensão do arquivo (exemplo: PDF, DOCX, etc.)
        valid_extensions = ["pdf", "doc", "docx"]
        extension = value.name.split(".")[-1].lower()
        if extension not in valid_extensions:
            raise ValidationError("Arquivo deve ser um PDF, DOC ou DOCX.")
        return value

    def save(self, **kwargs):
        arquivo = self.validated_data.get("arquivo")
        # Manipular o upload
        nome_arquivo = f"{str(uuid.uuid4())}_{arquivo.name}"
        file_path = f"processos/{nome_arquivo}"

        # Usar o default_storage para salvar o arquivo
        with default_storage.open(file_path, "wb+") as destination:
            for chunk in arquivo.chunks():
                destination.write(chunk)

        # Agora criamos o processo com o arquivo salvo
        self.validated_data["arquivo"] = file_path
        return super().save(**kwargs)
