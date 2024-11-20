from fpdf import FPDF
import os
from pathlib import Path


# Classe para gerar PDFs
class PDFGenerator(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Processo Administrativo/Fiscal", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")


# Função para criar processos fictícios
def generate_fictional_processes():
    processes = [
        {
            "tipo": "Administrativo",
            "conteudo": (
                "Processo Administrativo nº 2024/0001\n"
                "Requerente: João da Silva\n"
                "Objeto: Pedido de licença para reforma de imóvel localizado na Rua das Flores, nº 123.\n"
                "Data: 15/11/2024\n"
                "Solicitação: O requerente solicita autorização para realizar obras de reforma estrutural no referido imóvel.\n"
                "Justificativa: Imóvel apresenta problemas estruturais que colocam em risco a segurança.\n"
            ),
            "filename": "processo_administrativo_joao_silva.pdf",
        },
        {
            "tipo": "Administrativo",
            "conteudo": (
                "Processo Administrativo nº 2024/0002\n"
                "Requerente: Maria Oliveira\n"
                "Objeto: Solicitação de reabertura de prazo para apresentação de documentos relativos à regularização de empreendimento.\n"
                "Data: 17/11/2024\n"
                "Solicitação: Prorrogação de prazo em mais 15 dias úteis para entrega de documentação.\n"
                "Justificativa: Dificuldades na obtenção de certidões em cartório.\n"
            ),
            "filename": "processo_administrativo_maria_oliveira.pdf",
        },
        {
            "tipo": "Fiscal",
            "conteudo": (
                "Processo Fiscal nº 2024/0003\n"
                "Contribuinte: Empresa XYZ Ltda.\n"
                "Objeto: Notificação de débito referente ao não pagamento do ISS no exercício de 2023.\n"
                "Data: 18/11/2024\n"
                "Notificação: O contribuinte é notificado a regularizar o débito no valor de R$ 25.000,00, acrescido de multas e juros.\n"
                "Prazo: 30 dias úteis para pagamento ou apresentação de defesa.\n"
            ),
            "filename": "processo_fiscal_empresa_xyz.pdf",
        },
        {
            "tipo": "Fiscal",
            "conteudo": (
                "Processo Fiscal nº 2024/0004\n"
                "Contribuinte: Antônio Ferreira ME\n"
                "Objeto: Auto de infração por omissão de receita tributável no exercício de 2022.\n"
                "Data: 19/11/2024\n"
                "Notificação: Contribuinte deverá apresentar justificativa e documentos comprobatórios no prazo de 20 dias úteis.\n"
                "Valor: R$ 10.500,00\n"
            ),
            "filename": "processo_fiscal_antonio_ferreira.pdf",
        },
    ]

    data_dir = Path("mnt/data")
    data_dir.mkdir(parents=True, exist_ok=True)

    for process in processes:
        pdf = PDFGenerator()
        pdf.add_page()
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, process["conteudo"])
        pdf.output(data_dir / process["filename"])


# Gerar os PDFs fictícios
generate_fictional_processes()

# Listar os arquivos gerados
import os

generated_files = [f for f in os.listdir("/mnt/data") if f.endswith(".pdf")]
print(generated_files)
