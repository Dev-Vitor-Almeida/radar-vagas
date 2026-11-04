from sources.github import buscar_vagas_github
from services.filters import filtrar_vagas
from services.duplicate import filtrar_duplicadas, registrar_vagas
from services.telegram import enviar_mensagem


def main():
    print("Buscando vagas no GitHub...\n")

    vagas = buscar_vagas_github()

    print(f"Vagas encontradas: {len(vagas)}")

    vagas_filtradas = filtrar_vagas(vagas)

    print(f"Vagas após o filtro: {len(vagas_filtradas)}")

    vagas_novas = filtrar_duplicadas(vagas_filtradas)

    print(f"Vagas novas (sem duplicadas): {len(vagas_novas)}\n")

    vagas_enviadas = []

    for vaga in vagas_novas:
        mensagem = (
            f"📢 NOVA VAGA ENCONTRADA!\n\n"
            f"💼 {vaga['titulo']}\n"
            f"📂 Categoria: {vaga['categoria']}\n"
            f"🏢 Fonte: {vaga['fonte']}\n\n"
            f"🔗 {vaga['link']}"
        )

        sucesso = enviar_mensagem(mensagem)

        if sucesso:
            vagas_enviadas.append(vaga)
            print(f"Enviada: {vaga['titulo']}")
        else:
            print(f"Falha no envio: {vaga['titulo']}")

    registrar_vagas(vagas_enviadas)

    print(f"\nNotificações enviadas: {len(vagas_enviadas)}")
    print(f"Falhas no envio: {len(vagas_novas) - len(vagas_enviadas)}")

    print("\nBusca finalizada!")


if __name__ == "__main__":
    main()