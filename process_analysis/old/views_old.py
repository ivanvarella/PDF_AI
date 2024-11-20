from django.shortcuts import render, redirect
from .forms import ProcessForm
from .models import Process
from .utils import *


def upload_process(request):
    if request.method == "POST":
        print("teste3")
        form = ProcessForm(request.POST, request.FILES)
        if form.is_valid():
            print("teste")
            process = form.save()

            # Extrair texto do PDF
            filepath = process.arquivo.path
            text = extract_text_from_pdf(filepath)

            # Processar texto
            parts, demands = extract_parts_and_demands(text)
            resumo = summarize_with_gemini(text)
            resposta = suggest_response_with_gemini(text, parts, demands)

            # Salvar no modelo
            process.descricao = text
            process.partes = parts
            process.demandas = demands
            process.resumo = resumo
            process.resposta = resposta
            process.save()

            return redirect("process_list")
    else:
        form = ProcessForm()
        print("teste2")

    return render(request, "upload.html", {"form": form})


def process_list(request):
    processes = Process.objects.all()
    return render(request, "process_list.html", {"processes": processes})
