from PyPDF2 import PdfReader
import spacy
import re
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser

# Carregar variáveis de ambiente
from environ import Env

env = Env()
env.read_env(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

# Variáveis de ambiente
GOOGLE_API_KEY = env("GOOGLE_API_KEY")

# Carregar o modelo do Spacy
nlp = spacy.load("pt_core_news_sm")


def extract_text_from_pdf(filepath):
    """Extrai texto de um PDF"""
    reader = PdfReader(filepath)
    text = "".join(page.extract_text() for page in reader.pages)
    return text


def extract_parts_and_demands(text):
    """Extrai partes e demandas de um texto jurídico"""
    doc = nlp(text)
    parts = {"autor": None, "réu": None}
    demands = []

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            if not parts["autor"]:
                parts["autor"] = ent.text
            elif not parts["réu"]:
                parts["réu"] = ent.text

    demand_patterns = r"(indenização|restituição|rescisão|reparação|licença)"
    demands = re.findall(demand_patterns, text, flags=re.IGNORECASE)

    return parts, demands


def summarize_with_gemini(text):
    """Gera resumo do texto usando Gemini"""

    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
    prompt = PromptTemplate.from_template(
        "Você é um assistente jurídico especializado em resumos. Resuma o seguinte texto: {texto}"
    )

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({"texto": text})

    return response


def suggest_response_with_gemini(text, parts, demands):
    """Gera uma sugestão de resposta jurídica com Gemini"""

    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
    prompt = PromptTemplate.from_template(
        template="""
        **Texto do processo:**
        {texto}

        **Partes envolvidas:**
        Autor: {autor}
        Réu: {réu}

        **Demandas identificadas:**
        {demandas}

        **Com base nisso, forneça uma sugestão para a resposta da Procuradoria Geral Municipal.**
        """
    )

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke(
        {
            "texto": text,
            "autor": parts["autor"],
            "réu": parts["réu"],
            "demandas": ", ".join(demands),
        }
    )

    return response
