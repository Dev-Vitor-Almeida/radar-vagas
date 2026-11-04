
import requests

# Repositórios públicos que divulgam vagas de tecnologia
REPOSITORIOS = [
    "frontendbr/vagas",
    "react-brasil/vagas"
]


def buscar_vagas_github():
    vagas_encontradas = []

    for repositorio in REPOSITORIOS:
        url = f"https://api.github.com/repos/{repositorio}/issues"

        parametros = {
            "state": "open",
            "per_page": 100,
            "sort": "created",
            "direction": "desc"
        }

        try:
            resposta = requests.get(
                url,
                params=parametros,
                timeout=15
            )

            resposta.raise_for_status()
            vagas = resposta.json()

            for vaga in vagas:

                # Ignora pull requests e avisos dos repositórios
                if "pull_request" in vaga:
                    continue

                if "ATENÇÃO" in vaga["title"].upper():
                    continue

                vagas_encontradas.append({
                    "titulo": vaga["title"],
                    "descricao": vaga.get("body") or "",
                    "link": vaga["html_url"],
                    "fonte": repositorio,
                    "data_publicacao": vaga["created_at"]
                })

        except requests.RequestException as erro:
            print(f"Erro ao consultar {repositorio}: {erro}")

    return vagas_encontradas


if __name__ == "__main__":
    vagas = buscar_vagas_github()

    print(f"\nTotal de vagas encontradas: {len(vagas)}\n")

    for vaga in vagas[:10]:
        print("-" * 50)
        print(f"Título: {vaga['titulo']}")
        print(f"Fonte: {vaga['fonte']}")
        print(f"Link: {vaga['link']}")
