import os
import requests
from dotenv import load_dotenv

# Carrega as configurações do arquivo .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_mensagem(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    dados = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }

    resposta = requests.post(url, data=dados)
    resposta.raise_for_status()

    return resposta.json()


if __name__ == "__main__":
    enviar_mensagem(
        "🚀 Radar de Vagas iniciado!\n\n"
        "Nosso sistema já consegue enviar notificações!"
    )

    print("Mensagem enviada com sucesso!")
