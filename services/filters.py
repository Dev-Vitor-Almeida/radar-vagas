
import re
import unicodedata


LOCALIZACOES_ACEITAS = [
    "sao paulo",
    "taboao da serra",
    "embu das artes",
    "osasco",
]

LOCALIZACOES_PROIBIDAS_IDENTIFICADAS = [
    "diadema",
    "curitiba",
    "ribeirao preto",
    "pouso alegre",
    "pato branco",
]

INDICADORES_VAGA_REMOTA = [
    "trabalho remoto",
    "vaga remota",
    "vaga remoto",
    "100% remoto",
    "100% remota",
    "modelo remoto",
    "modelo de trabalho remoto",
    "regime remoto",
    "regime de trabalho remoto",
    "modalidade remota",
    "atuacao remota",
    "posicao remota",
    "home office",
    "teletrabalho",
]

TERMOS_BRASIL = [
    "todo o brasil",
    "todo brasil",
    "qualquer lugar do brasil",
    "todo territorio nacional",
    "brasil inteiro",
    "candidatos de todo o brasil",
    "candidatos de qualquer estado",
    "qualquer estado do brasil",
    "em todo o territorio nacional",
    "residir em qualquer estado",
    "para todo o territorio brasileiro",
    "de qualquer regiao do brasil",
    "vaga para todo o brasil",
    "vaga para todo brasil",
]

TERMOS_RESTRICAO = [
    "exclusivo para residentes de",
    "somente residentes de",
    "apenas residentes de",
    "residir obrigatoriamente em",
    "residencia obrigatoria em",
    "vaga exclusiva para",
]

TERMOS_TI = [
    "tecnologia da informacao",
    "desenvolvedor",
    "desenvolvedora",
    "software",
    "front-end",
    "frontend",
    "back-end",
    "backend",
    "fullstack",
    "full stack",
    "react",
    "javascript",
    "python",
    "java",
    "node.js",
    "suporte tecnico",
    "suporte ti",
    "service desk",
    "help desk",
    "infraestrutura de ti",
    "infraestrutura de redes",
    "redes de computadores",
    "hardware",
    "analista de sistemas",
    "sistemas de informacao",
    "banco de dados",
    "cloud",
    "devops",
    "qa",
    "tester",
    "seguranca da informacao",
    "seguranca cibernetica",
    "estagio em ti",
    "estagiario de ti",
    "estagiaria de ti",
    "assistente de ti",
    "auxiliar de ti",
    "tecnico de informatica",
    "tecnico em informatica",
    "analista de suporte",
]

TERMOS_PROGRAMACAO_TI = [
    "javascript",
    "typescript",
    "python",
    "java",
    "node.js",
    "c#",
    ".net",
    "php",
    "ruby",
    "golang",
    "kotlin",
    "swift",
    "c++",
    "react",
    "angular",
    "vue.js",
    "html",
    "css",
    "sql",
    "desenvolvimento de software",
    "desenvolvimento web",
    "linguagem de programacao",
    "programacao orientada a objetos",
    "programacao de sistemas",
    "desenvolvimento de aplicacoes",
]

TERMOS_COMERCIAIS = [
    "sales",
    "vendas",
    "comercial",
    "vendedor",
    "vendedora",
    "representante comercial",
]

TERMOS_ADMIN = [
    "auxiliar administrativo",
    "assistente administrativo",
    "analista administrativo",
    "administrativo",
    "assistente de escritorio",
    "auxiliar de escritorio",
    "secretaria",
    "recepcionista",
    "assistente de operacoes",
]

TERMOS_EXCLUIDOS = [
    "pl",
    "pleno",
    "senior",
    "sr",
    "tech lead",
    "team lead",
    "coordenador",
    "coordenadora",
    "gerente",
    "gerencia",
    "especialista",
    "staff engineer",
    "principal engineer",
    "head de",
    "diretor",
    "diretora",
    "supervisor",
    "supervisora",
]

TERMOS_TECNICOS_INFRA = [
    "servidores",
    "windows server",
    "linux",
    "firewall",
    "cisco",
    "vmware",
    "active directory",
    "data center",
    "datacenter",
    "redes",
    "cloud",
    "aws",
    "azure",
    "infraestrutura de ti",
    "suporte ti",
    "tecnologia da informacao",
]

TERMOS_VAGA_TESTE = [
    "[modelo]",
    "teste convocacao",
    "vaga de teste",
    "anuncio de teste",
]


def normalizar(texto):
    texto = str(texto).lower()
    texto = unicodedata.normalize("NFD", texto)

    return "".join(
        caractere for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )


def contem_termo(texto, termo):
    padrao = r"(?<!\w)" + re.escape(termo) + r"(?!\w)"
    return re.search(padrao, texto) is not None


def titulo_tem_local_proibido(titulo):
    titulo = normalizar(titulo)

    return any(
        contem_termo(titulo, local)
        for local in LOCALIZACOES_PROIBIDAS_IDENTIFICADAS
    )


def titulo_indica_remoto(titulo):
    titulo = normalizar(titulo)

    return any(
        contem_termo(titulo, termo)
        for termo in ["remoto", "remota", "remote"]
    ) or "home office" in titulo


def descricao_indica_remoto(descricao):
    descricao = normalizar(descricao)

    return any(
        termo in descricao
        for termo in INDICADORES_VAGA_REMOTA
    )


def aceita_trabalho_nacional(titulo, descricao):
    texto = normalizar(titulo + " " + descricao)

    aceita_brasil_todo = any(
        termo in texto for termo in TERMOS_BRASIL
    )

    tem_restricao = any(
        termo in texto for termo in TERMOS_RESTRICAO
    )

    return aceita_brasil_todo and not tem_restricao


def verificar_vaga_remota(titulo, descricao):
    eh_remota = (
        titulo_indica_remoto(titulo)
        or descricao_indica_remoto(descricao)
    )

    if not eh_remota:
        return None

    return aceita_trabalho_nacional(titulo, descricao)


def verificar_localizacao(titulo, descricao, vaga):
    titulo_normalizado = normalizar(titulo)
    descricao_normalizada = normalizar(descricao)

    cidade = normalizar(vaga.get("cidade", "")).strip()
    estado = normalizar(vaga.get("estado", "")).strip()
    modalidade = normalizar(vaga.get("modalidade", "")).strip()
    fonte = vaga.get("fonte", "")

    if titulo_tem_local_proibido(titulo_normalizado):
        return False

    if fonte == "Gupy":
        if modalidade == "remote":
            return aceita_trabalho_nacional(
                titulo_normalizado,
                descricao_normalizada
            )

        if modalidade in ["hybrid", "on-site"]:
            return (
                cidade in LOCALIZACOES_ACEITAS
                and estado == "sao paulo"
            )

        return False

    if fonte == "Empregando Brasil":
        # O título remoto pode identificar uma exceção à localização.
        if titulo_indica_remoto(titulo_normalizado):
            return aceita_trabalho_nacional(
                titulo_normalizado,
                descricao_normalizada
            )

        # Com cidade e estado preenchidos, eles são a referência principal.
        if cidade or estado:
            return (
                cidade in LOCALIZACOES_ACEITAS
                and estado in ["sp", "sao paulo"]
            )

        # Sem localização, exigimos indicação explícita de trabalho remoto.
        return (
            descricao_indica_remoto(descricao_normalizada)
            and aceita_trabalho_nacional(
                titulo_normalizado,
                descricao_normalizada
            )
        )

    resultado_remoto = verificar_vaga_remota(
        titulo_normalizado,
        descricao_normalizada
    )

    if resultado_remoto is not None:
        return resultado_remoto

    return any(
        contem_termo(titulo_normalizado, local)
        for local in LOCALIZACOES_ACEITAS
    )


def classificar_vaga(titulo, descricao):
    titulo = normalizar(titulo)
    descricao = normalizar(descricao)

    if any(
        contem_termo(titulo, termo)
        for termo in TERMOS_EXCLUIDOS
    ):
        return None

    if any(
        re.search(r"\b" + termo + r"\b", titulo)
        for termo in ["ii", "iii", "iv", "v"]
    ):
        if any(
            termo in titulo
            for termo in ["analista", "engenheiro", "especialista"]
        ):
            return None

    # Vagas comerciais não entram apenas por mencionar software.
    if any(
        contem_termo(titulo, termo)
        for termo in TERMOS_COMERCIAIS
    ):
        return None

    # Programação precisa ter relação com desenvolvimento de software.
    if (
        contem_termo(titulo, "programador")
        or contem_termo(titulo, "programadora")
        or contem_termo(titulo, "programacao")
    ):
        texto = titulo + " " + descricao

        if any(
            termo in texto
            for termo in ["cnc", "frota"]
        ):
            return None

        if any(
            termo in texto
            for termo in TERMOS_PROGRAMACAO_TI
        ):
            return {
                "categoria": "TI",
                "prioridade": 1
            }

        return None

    if any(
        contem_termo(titulo, termo)
        for termo in TERMOS_TI
    ):
        return {
            "categoria": "TI",
            "prioridade": 1
        }

    if contem_termo(titulo, "analista de infraestrutura"):
        texto = titulo + " " + descricao

        if any(
            termo in texto for termo in TERMOS_TECNICOS_INFRA
        ):
            return {
                "categoria": "TI",
                "prioridade": 1
            }

    if any(
        contem_termo(titulo, termo)
        for termo in TERMOS_ADMIN
    ):
        return {
            "categoria": "Administrativo",
            "prioridade": 2
        }

    return None


def filtrar_vagas(vagas):
    vagas_aprovadas = []
    links_processados = set()

    for vaga in vagas:
        titulo = vaga.get("titulo", "")
        descricao = vaga.get("descricao", "")

        titulo_normalizado = normalizar(titulo)

        if "aprendiz" in titulo_normalizado:
            continue

        if any(
            termo in titulo_normalizado
            for termo in TERMOS_VAGA_TESTE
        ):
            continue

        if not verificar_localizacao(titulo, descricao, vaga):
            continue

        classificacao = classificar_vaga(titulo, descricao)

        if classificacao is None:
            continue

        link = vaga.get("link")

        if link and link in links_processados:
            continue

        if link:
            links_processados.add(link)

        nova_vaga = vaga.copy()
        nova_vaga.update(classificacao)

        vagas_aprovadas.append(nova_vaga)

    vagas_aprovadas.sort(
        key=lambda vaga: vaga["prioridade"]
    )

    return vagas_aprovadas


if __name__ == "__main__":
    vagas_teste = [
        {
            "titulo": "Estágio em TI",
            "descricao": "Vaga presencial.",
            "fonte": "Gupy",
            "cidade": "São Paulo",
            "estado": "São Paulo",
            "modalidade": "hybrid"
        },
        {
            "titulo": "Estágio em TI",
            "descricao": "Vaga presencial.",
            "fonte": "Gupy",
            "cidade": "Curitiba",
            "estado": "Paraná",
            "modalidade": "on-site"
        },
        {
            "titulo": "Suporte Técnico N1",
            "descricao": "Atuação em São Paulo.",
            "fonte": "Gupy",
            "cidade": "Ribeirão Preto",
            "estado": "São Paulo",
            "modalidade": "on-site"
        },
        {
            "titulo": "Estágio em Governança de TI",
            "descricao": "Trabalho remoto para todo o Brasil.",
            "fonte": "Gupy",
            "cidade": "",
            "estado": "",
            "modalidade": "remote"
        },
        {
            "titulo": "Estágio em TI",
            "descricao": "Trabalho remoto.",
            "fonte": "Gupy",
            "cidade": "",
            "estado": "",
            "modalidade": "remote"
        },
        {
            "titulo": "[Remoto] Estágio em Desenvolvimento Java",
            "descricao": "Vaga para todo o Brasil.",
            "fonte": "GitHub"
        },
        {
            "titulo": "[Presencial - Osasco] Auxiliar Administrativo",
            "descricao": "Rotinas administrativas.",
            "fonte": "GitHub"
        },
        {
            "titulo": "[Presencial - Diadema] Auxiliar Administrativo",
            "descricao": "Rotinas administrativas.",
            "fonte": "GitHub"
        },
        {
            "titulo": "[Presencial - São Paulo] Engenheiro de Produção",
            "descricao": "Infraestrutura aeroportuária.",
            "fonte": "GitHub"
        },
        {
            "titulo": "[Remoto] Analista de Suporte TI SR",
            "descricao": "Vaga para todo o Brasil.",
            "fonte": "GitHub"
        },
        {
            "titulo": "Desenvolvedor Java PL",
            "descricao": "Vaga híbrida.",
            "fonte": "Gupy",
            "cidade": "São Paulo",
            "estado": "São Paulo",
            "modalidade": "hybrid"
        },
        {
            "titulo": "Analista de Infraestrutura de Redes PL",
            "descricao": "Vaga presencial.",
            "fonte": "Gupy",
            "cidade": "Taboão da Serra",
            "estado": "São Paulo",
            "modalidade": "on-site"
        },
        {
            "titulo": "[Modelo] Pessoa Desenvolvedora Fullstack - TESTE CONVOCAÇÃO",
            "descricao": "Vaga presencial.",
            "fonte": "Gupy",
            "cidade": "São Paulo",
            "estado": "São Paulo",
            "modalidade": "on-site"
        },
        {
            "titulo": "Auxiliar Administrativo - Diadema",
            "descricao": "Vaga presencial.",
            "fonte": "Gupy",
            "cidade": "São Paulo",
            "estado": "São Paulo",
            "modalidade": "on-site"
        },
        {
            "titulo": "Assistente de TI",
            "descricao": "Atuação presencial.",
            "fonte": "Empregando Brasil",
            "cidade": "São Paulo",
            "estado": "SP"
        },
        {
            "titulo": "Assistente de TI",
            "descricao": "Atuação presencial.",
            "fonte": "Empregando Brasil",
            "cidade": "Barueri",
            "estado": "SP"
        },
        {
            "titulo": "Estágio em TI",
            "descricao": "Trabalho remoto para todo o Brasil.",
            "fonte": "Empregando Brasil",
            "cidade": "",
            "estado": ""
        },
        {
            "titulo": "Estágio em TI",
            "descricao": "Trabalho remoto.",
            "fonte": "Empregando Brasil",
            "cidade": "",
            "estado": ""
        },
        {
            "titulo": "Programador CNC",
            "descricao": "Programação e operação de máquinas CNC.",
            "fonte": "Empregando Brasil",
            "cidade": "São Paulo",
            "estado": "SP"
        },
        {
            "titulo": "Programador de frota",
            "descricao": "Organização e programação de veículos da frota.",
            "fonte": "Empregando Brasil",
            "cidade": "São Paulo",
            "estado": "SP"
        },
        {
            "titulo": "Analista de Suporte ao Cliente Latam - Espanhol",
            "descricao": "Atendimento ao cliente com suporte remoto. Vaga para todo o Brasil.",
            "fonte": "Empregando Brasil",
            "cidade": "Rio de Janeiro",
            "estado": "RJ"
        },
        {
            "titulo": "Software Sales Representative",
            "descricao": "Responsável por vendas de software.",
            "fonte": "Empregando Brasil",
            "cidade": "São Paulo",
            "estado": "SP"
        },
        {
            "titulo": "Assistente de Programação",
            "descricao": "Apoio ao desenvolvimento de sistemas em Java.",
            "fonte": "Empregando Brasil",
            "cidade": "São Paulo",
            "estado": "SP"
        }
    ]

    resultado = filtrar_vagas(vagas_teste)

    print("\nRESULTADO DO TESTE")
    print("-" * 50)

    for vaga in resultado:
        print(f"Título: {vaga['titulo']}")
        print(f"Categoria: {vaga['categoria']}")
        print(f"Prioridade: {vaga['prioridade']}")
        print("-" * 50)

    print(f"Total aprovado: {len(resultado)}")
    print(f"Total rejeitado: {len(vagas_teste) - len(resultado)}")
