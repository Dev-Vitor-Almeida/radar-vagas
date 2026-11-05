import os
import requests
from dotenv import load_dotenv

# Carrega as configurações do arquivo .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def enviar_mensagem(mensagem):
    if not TOKEN or not CHAT_ID:
        print("Erro: Token ou Chat ID não configurado.")
        return False

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    dados = {
        "chat_id": CHAT_ID,
        "text": mensagem,
        "disable_web_page_preview": True
    }

    try:
        resposta = requests.post(
            url,
            data=dados,
            timeout=15
        )

        resposta.raise_for_status()
        resultado = resposta.json()

        if resultado.get("ok"):
            return True

        print("O Telegram não confirmou o envio.")
        return False

    except requests.RequestException as erro:
        print(f"Erro ao enviar mensagem: {erro}")
        return False


# Teste da integração com o Telegram
#if __name__ == "__main__":
    sucesso = enviar_mensagem(
        "🚀 Teste do Radar de Vagas!\n\n"
        "Integração com o Telegram funcionando."
    )

    if sucesso:
        print("Mensagem enviada com sucesso!")
    else:
        print("Não foi possível enviar a mensagem.")