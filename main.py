
from sources.github import buscar_vagas_github
from sources.gupy import buscar_vagas_gupy
from sources.empregandobrasil import buscar_vagas_empregando_brasil
from services.filters import filtrar_vagas
from services.duplicate import filtrar_duplicadas, registrar_vagas
from services.telegram import enviar_mensagem


# True: apenas testa | False: envia as notificações
MODO_TESTE = True


def main():
    print("Iniciando Radar de Vagas...\n")

    print("Buscando vagas no GitHub...\n")
    vagas_github = buscar_vagas_github()
    print(f"Vagas encontradas no GitHub: {len(vagas_github)}\n")

    print("Buscando vagas na Gupy...\n")
    vagas_gupy = buscar_vagas_gupy()
    print(f"\nVagas encontradas na Gupy: {len(vagas_gupy)}")

    print("\nBuscando vagas no Empregando Brasil...\n")
    vagas_empregando = buscar_vagas_empregando_brasil()
    print(
        "\nVagas encontradas no Empregando Brasil: "
        f"{len(vagas_empregando)}"
    )

    vagas = vagas_github + vagas_gupy + vagas_empregando
    print(f"\nTotal de vagas encontradas: {len(vagas)}")

    vagas_filtradas = filtrar_vagas(vagas)
    print(f"\nVagas aprovadas pelo filtro: {len(vagas_filtradas)}")

    # Remove vagas que já foram enviadas anteriormente
    vagas_novas = filtrar_duplicadas(vagas_filtradas)
    print(f"Vagas novas, sem duplicadas: {len(vagas_novas)}")

    if MODO_TESTE:
        print("\n========================================")
        print("MODO DE TESTE - NENHUMA MENSAGEM ENVIADA")
        print("========================================\n")

        for vaga in vagas_novas:
            print(f"Título: {vaga['titulo']}")
            print(f"Categoria: {vaga['categoria']}")
            print(f"Fonte: {vaga['fonte']}")
            print(f"Empresa: {vaga.get('empresa', 'Não informada')}")
            print(f"Cidade: {vaga.get('cidade', 'Não informada')}")
            print(f"Estado: {vaga.get('estado', 'Não informado')}")
            print(f"Modalidade: {vaga.get('modalidade') or 'Não informada'}")
            print(f"Link: {vaga['link']}")
            print("-" * 60)

        print("\nRESUMO")
        print(f"Total aprovado: {len(vagas_filtradas)}")
        print(f"Vagas novas: {len(vagas_novas)}")
        print("Histórico preservado.")
        print("Telegram não foi acionado.")

        return

    vagas_enviadas = []

    for vaga in vagas_novas:
        mensagem = (
            "📢 NOVA VAGA ENCONTRADA!\n\n"
            f"💼 {vaga['titulo']}\n"
            f"📂 Categoria: {vaga['categoria']}\n"
            f"🏢 Fonte: {vaga['fonte']}\n"
            f"🏭 Empresa: {vaga.get('empresa') or 'Não informada'}\n"
            f"📍 Local: {vaga.get('cidade') or 'Não informado'}"
            f" - {vaga.get('estado') or 'Não informado'}\n"
            f"💻 Modalidade: {vaga.get('modalidade') or 'Não informada'}\n\n"
            f"🔗 {vaga['link']}"
        )

        sucesso = enviar_mensagem(mensagem)

        if sucesso:
            vagas_enviadas.append(vaga)
            print(f"Enviada: {vaga['titulo']}")
        else:
            print(f"Falha no envio: {vaga['titulo']}")

    # Registra apenas as notificações confirmadas pelo Telegram
    registrar_vagas(vagas_enviadas)

    print("\n========================================")
    print("RESUMO DO ENVIO")
    print("========================================")
    print(f"Vagas novas: {len(vagas_novas)}")
    print(f"Notificações enviadas: {len(vagas_enviadas)}")
    print(f"Falhas no envio: {len(vagas_novas) - len(vagas_enviadas)}")
    print("\nBusca finalizada!")


if __name__ == "__main__":
    main()
