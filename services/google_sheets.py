
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_SHEETS_URL = os.getenv("GOOGLE_SHEETS_URL")
GOOGLE_SHEETS_TOKEN = os.getenv("GOOGLE_SHEETS_TOKEN")


def enviar_requisicao(dados):
    if not GOOGLE_SHEETS_URL or not GOOGLE_SHEETS_TOKEN:
        raise RuntimeError(
            "Configure GOOGLE_SHEETS_URL e GOOGLE_SHEETS_TOKEN no .env"
        )

    dados["token"] = GOOGLE_SHEETS_TOKEN

    try:
        resposta = requests.post(
            GOOGLE_SHEETS_URL,
            json=dados,
            timeout=30
        )

        resposta.raise_for_status()
        resultado = resposta.json()

        if not resultado.get("sucesso"):
            raise RuntimeError(
                resultado.get("erro", "Erro na comunicação com a planilha.")
            )

        return resultado

    except requests.RequestException as erro:
        raise RuntimeError(
            f"Falha ao acessar o Google Planilhas: {erro}"
        ) from erro

    except ValueError as erro:
        raise RuntimeError(
            "O Google Planilhas retornou uma resposta inválida."
        ) from erro


def consultar_links():
    resultado = enviar_requisicao({
        "acao": "consultar_links"
    })

    return set(resultado.get("links", []))


def salvar_vagas(vagas):
    if not vagas:
        return {
            "sucesso": True,
            "recebidas": 0,
            "salvas": 0,
            "duplicadas": 0
        }

    resultado = enviar_requisicao({
        "acao": "salvar_vagas",
        "vagas": [
            {
                "empresa": vaga.get("empresa"),
                "titulo": vaga.get("titulo"),
                "salario_beneficios": vaga.get("salario_beneficios"),
                "link": vaga.get("link"),
                "categoria": vaga.get("categoria")
            }
            for vaga in vagas
        ]
    })

    return resultado
