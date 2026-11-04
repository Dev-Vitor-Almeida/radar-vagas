
import json
import os

ARQUIVO_DUPLICADAS = "database/vagas_processadas.json"


def carregar_vagas_processadas():
    if not os.path.exists(ARQUIVO_DUPLICADAS):
        return []

    try:
        with open(ARQUIVO_DUPLICADAS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except (json.JSONDecodeError, OSError):
        return []


def filtrar_duplicadas(vagas):
    vagas_processadas = carregar_vagas_processadas()
    links_existentes = set(vagas_processadas)

    vagas_novas = []

    for vaga in vagas:
        link = vaga.get("link")

        if link and link not in links_existentes:
            vagas_novas.append(vaga)
            links_existentes.add(link)

    return vagas_novas


def registrar_vagas(vagas):
    vagas_processadas = carregar_vagas_processadas()

    links_existentes = set(vagas_processadas)

    for vaga in vagas:
        link = vaga.get("link")

        if link:
            links_existentes.add(link)

    os.makedirs("database", exist_ok=True)

    with open(ARQUIVO_DUPLICADAS, "w", encoding="utf-8") as arquivo:
        json.dump(
            list(links_existentes),
            arquivo,
            ensure_ascii=False,
            indent=4
        )


if __name__ == "__main__":
    vagas_teste = [
        {
            "titulo": "Estágio em TI",
            "link": "https://exemplo.com/vaga/1"
        },
        {
            "titulo": "Suporte Técnico",
            "link": "https://exemplo.com/vaga/2"
        }
    ]

    # Primeira execução: as duas vagas são novas
    novas = filtrar_duplicadas(vagas_teste)

    print(f"Primeira execução: {len(novas)} vagas novas")

    # Registra as vagas encontradas
    registrar_vagas(novas)

    # Segunda execução: as mesmas vagas já foram registradas
    repetidas = filtrar_duplicadas(vagas_teste)

    print(f"Segunda execução: {len(repetidas)} vagas novas")
