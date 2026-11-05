
from services.google_sheets import consultar_links, salvar_vagas


def filtrar_duplicadas(vagas):
    links_existentes = consultar_links()

    vagas_novas = []

    for vaga in vagas:
        link = vaga.get("link")

        if link and link not in links_existentes:
            vagas_novas.append(vaga)
            links_existentes.add(link)

    return vagas_novas


def registrar_vagas(vagas):
    if not vagas:
        return {
            "sucesso": True,
            "salvas": 0,
            "duplicadas": 0
        }

    return salvar_vagas(vagas)
