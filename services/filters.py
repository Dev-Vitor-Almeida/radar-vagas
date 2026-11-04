
import unicodedata


LOCALIZACOES_ACEITAS = [
    "sao paulo",
    "grande sao paulo",
    "regiao metropolitana de sao paulo",
    "taboao da serra",
    "embu das artes",
    "osasco",
]

LOCALIZACOES_FORA = [
    "curitiba",
    "belo horizonte",
    "rio de janeiro",
    "brasilia",
    "porto alegre",
    "recife",
    "salvador",
    "fortaleza",
]

TERMOS_REMOTOS = [
    "remoto",
    "remota",
    "remote",
    "home office",
]

TERMOS_BRASIL = [
    "todo o brasil",
    "todo brasil",
    "qualquer lugar do brasil",
    "todo territorio nacional",
    "brasil inteiro",
    "candidatos de todo o brasil",
]

# Áreas de tecnologia
TERMOS_TI = [
    "tecnologia",
    "ti",
    "desenvolvedor",
    "desenvolvimento",
    "programador",
    "programacao",
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
    "infraestrutura",
    "redes",
    "hardware",
    "analista de sistemas",
    "sistemas",
    "banco de dados",
    "dados",
    "cloud",
    "devops",
    "qa",
    "tester",
    "seguranca da informacao",
]

# Áreas administrativas
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

# Níveis e cargos que não fazem parte do nosso foco inicial
TERMOS_EXCLUIDOS = [
    "pleno",
    "senior",
    "tech lead",
    "team lead",
    "coordenador",
    "coordenadora",
    "gerente",
    "gerencia",
    "especialista",
    "staff engineer",
    "principal engineer",
]


def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)

    return "".join(
        caractere for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )


def verificar_localizacao(titulo, descricao):
    texto = titulo + " " + descricao

    eh_remota = any(
        termo in titulo for termo in TERMOS_REMOTOS
    )

    local_fora = any(
        local in titulo for local in LOCALIZACOES_FORA
    )

    local_aceita = any(
        local in titulo for local in LOCALIZACOES_ACEITAS
    )

    aceita_brasil_todo = any(
        termo in texto for termo in TERMOS_BRASIL
    )

    # Vagas remotas podem ser de qualquer estado
    if eh_remota:
        if local_fora and not aceita_brasil_todo:
            return False

        return True

    # Vagas presenciais, híbridas ou com local definido
    # precisam estar na nossa região
    if local_aceita:
        return True

    return False



def classificar_vaga(titulo):
    titulo = normalizar(titulo)

    if any(termo in titulo for termo in TERMOS_EXCLUIDOS):
        return None

    # Verifica TI sem procurar a sequência "ti" dentro de outras palavras
    palavras = titulo.replace("-", " ").replace("/", " ").split()

    termos_ti = [
        termo for termo in TERMOS_TI
        if termo != "ti"
    ]

    if "ti" in palavras or any(
        termo in titulo for termo in termos_ti
    ):
        return {
            "categoria": "TI",
            "prioridade": 1
        }

    if any(termo in titulo for termo in TERMOS_ADMIN):
        return {
            "categoria": "Administrativo",
            "prioridade": 2
        }

    return None


def filtrar_vagas(vagas):
    vagas_aprovadas = []

    for vaga in vagas:
        titulo = normalizar(vaga.get("titulo", ""))
        descricao = normalizar(vaga.get("descricao", ""))

        # Exclui Jovem Aprendiz
        if "aprendiz" in titulo:
            continue

        if not verificar_localizacao(titulo, descricao):
            continue

        classificacao = classificar_vaga(titulo)

        if classificacao is None:
            continue

        nova_vaga = vaga.copy()
        nova_vaga.update(classificacao)

        vagas_aprovadas.append(nova_vaga)

    # TI primeiro, administrativo depois
    vagas_aprovadas.sort(key=lambda vaga: vaga["prioridade"])

    return vagas_aprovadas


if __name__ == "__main__":
    vagas_teste = [
        {
            "titulo": "[Remoto] Estágio em Desenvolvimento Java",
            "descricao": "Vaga para todo o Brasil."
        },
        {
            "titulo": "[Híbrido - São Paulo] Suporte Técnico N1",
            "descricao": "Atendimento presencial."
        },
        {
            "titulo": "[Presencial - Osasco] Auxiliar Administrativo",
            "descricao": "Rotinas administrativas."
        },
        {
            "titulo": "[Remoto] Assistente Administrativo",
            "descricao": "Vaga para todo o Brasil."
        },
        {
            "titulo": "[Remoto] Senior Software Engineer",
            "descricao": "Vaga para todo o Brasil."
        },
        {
            "titulo": "[Remoto] Tech Lead Java",
            "descricao": "Vaga para todo o Brasil."
        },
        {
            "titulo": "[Presencial - São Paulo] Jovem Aprendiz TI",
            "descricao": "Vaga presencial."
        },
        {
            "titulo": "[Híbrido - Curitiba] Desenvolvedor Java",
            "descricao": "Vaga híbrida."
        },
        {
            "titulo": "[Remoto] Auxiliar de Limpeza",
            "descricao": "Vaga para todo o Brasil."
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
