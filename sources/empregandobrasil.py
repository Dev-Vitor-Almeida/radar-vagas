
import re
import html
import requests
import xml.etree.ElementTree as ET


URL = "https://empregandobrasil.com.br/feeds/partners/jobs.xml"


def limpar_descricao(descricao):
    descricao = html.unescape(descricao or "")
    descricao = re.sub(r"<[^>]+>", " ", descricao)
    return re.sub(r"\s+", " ", descricao).strip()


def buscar_vagas_empregando_brasil():
    vagas_encontradas = []
    links_existentes = set()

    print("Pesquisando no Empregando Brasil...")

    try:
        resposta = requests.get(
            URL,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/xml"
            },
            timeout=30
        )

        resposta.raise_for_status()

        raiz = ET.fromstring(resposta.content)

        for elemento in raiz.iter():
            tag = elemento.tag.split("}")[-1]

            if tag != "job":
                continue

            dados = {
                filho.tag.split("}")[-1]: filho.text or ""
                for filho in elemento
            }

            link = dados.get("url", "").strip()

            if not link or link in links_existentes:
                continue

            links_existentes.add(link)

            vagas_encontradas.append({
                "titulo": dados.get("title", "").strip(),
                "descricao": limpar_descricao(
                    dados.get("description", "")
                ),
                "link": link,
                "fonte": "Empregando Brasil",
                "data_publicacao": (
                    dados.get("published", "")
                    or dados.get("created", "")
                ),
                "cidade": dados.get("city", "").strip(),
                "estado": dados.get("state", "").strip(),
                "modalidade": "",
                "empresa": dados.get("company", "").strip()
            })

        print(
            "Vagas encontradas no Empregando Brasil: "
            f"{len(vagas_encontradas)}"
        )

    except requests.RequestException as erro:
        print(f"Erro ao consultar Empregando Brasil: {erro}")

    except ET.ParseError as erro:
        print(f"Erro ao interpretar o XML: {erro}")

    return vagas_encontradas


if __name__ == "__main__":
    vagas = buscar_vagas_empregando_brasil()

    print("\n================================")
    print(f"Total de vagas encontradas: {len(vagas)}")
    print("================================\n")

    for vaga in vagas[:10]:
        print("Título:", vaga["titulo"])
        print("Empresa:", vaga["empresa"])
        print("Cidade:", vaga["cidade"])
        print("Estado:", vaga["estado"])
        print("Fonte:", vaga["fonte"])
        print("Link:", vaga["link"])
        print("-" * 50)
