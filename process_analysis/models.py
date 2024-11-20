from django.db import models


class Process(models.Model):
    # usuario = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    id_processo = models.AutoField(primary_key=True)
    arquivo = models.FileField(upload_to="pdfs/")
    descricao = models.TextField(blank=True, null=True)
    partes = models.JSONField(blank=True, null=True)
    demandas = models.JSONField(blank=True, null=True)
    resumo = models.TextField(blank=True, null=True)
    resposta = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Processo {self.id_processo} - {self.arquivo.nome}"
