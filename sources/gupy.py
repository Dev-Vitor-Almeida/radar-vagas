
import requests


URL = "https://portal.gupy.io/api/job-search/jobs"

TERMOS_BUSCA = [
    "estágio em TI",
    "suporte",
    "desenvolvedor",
    "desenvolvimento",
    "infraestrutura",
    "redes",
    "assistente de TI",
    "auxiliar administrativo",
    "assistente administrativo"
]

LIMITE_POR_PAGINA = 50
MAX_PAGINAS_POR_TERMO = 2


def buscar_vagas_gupy():
    vagas_encontradas = []
    links_existentes = set()

    for termo in TERMOS_BUSCA:
        print(f"Pesquisando na Gupy: {termo}")

        for pagina in range(MAX_PAGINAS_POR_TERMO):
            parametros = {
                "jobName": termo,
                "limit": LIMITE_POR_PAGINA,
                "offset": pagina * LIMITE_POR_PAGINA
            }

            try:
                resposta = requests.get(
                    URL,
                    params=parametros,
                    headers={
                        "User-Agent": "Mozilla/5.0",
                        "Accept": "application/json"
                    },
                    timeout=20
                )

                resposta.raise_for_status()
                dados = resposta.json()

                resultados = dados.get("data", [])

                if not resultados:
                    break

                for vaga in resultados:
                    link = vaga.get("jobUrl")

                    if not link or link in links_existentes:
                        continue

                    links_existentes.add(link)

                    vagas_encontradas.append({
                        "titulo": vaga.get("name", ""),
                        "descricao": vaga.get("description", ""),
                        "link": link,
                        "fonte": "Gupy",
                        "data_publicacao": vaga.get("publishedDate", ""),
                        "cidade": vaga.get("city", ""),
                        "estado": vaga.get("state", ""),
                        "modalidade": vaga.get("workplaceType", "")
                    })

                total = dados.get("pagination", {}).get("total", 0)

                if (pagina + 1) * LIMITE_POR_PAGINA >= total:
                    break

            except requests.RequestException as erro:
                print(f"Erro ao pesquisar '{termo}': {erro}")
                break

            except ValueError:
                print(f"Resposta inválida da Gupy para o termo: {termo}")
                break

    return vagas_encontradas


if __name__ == "__main__":
    vagas = buscar_vagas_gupy()

    print("\n================================")
    print(f"Total de vagas encontradas: {len(vagas)}")
    print("================================\n")

    for vaga in vagas[:10]:
        print("Título:", vaga["titulo"])
        print("Cidade:", vaga["cidade"])
        print("Estado:", vaga["estado"])
        print("Modalidade:", vaga["modalidade"])
        print("Fonte:", vaga["fonte"])
        print("Link:", vaga["link"])
        print("-" * 50)
