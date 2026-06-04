"""
Modulo NLP - Processamento de logs de missoes espaciais.
Extrai eventos, classifica severidade e identifica palavras-chave.
"""
import re
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Palavras de parada em portugues + ingles
try:
    STOPWORDS = set(stopwords.words("portuguese")) | set(stopwords.words("english"))
except Exception:
    STOPWORDS = set()

PALAVRAS_CRITICO = {"critico", "falha", "vazamento", "falhou", "critica", "emergencia"}
PALAVRAS_ALERTA  = {"alerta", "anomalo", "acima", "intermitente", "anomalia", "aviso"}
PALAVRAS_OK      = {"normalizado", "normal", "sucesso", "confirmada", "estavel", "restaurado"}

REGEX_EVENTO = re.compile(
    r"\[(\d{2}:\d{2})\]\s*(CRITICO|ALERTA|AVISO)?:?\s*(.*)",
    re.IGNORECASE,
)


def classificar_linha(texto: str) -> str:
    t = texto.lower()
    if any(p in t for p in PALAVRAS_CRITICO):
        return "CRITICO"
    if any(p in t for p in PALAVRAS_ALERTA):
        return "ALERTA"
    if any(p in t for p in PALAVRAS_OK):
        return "NORMAL"
    return "INFO"


def extrair_palavras_chave(texto: str, top_n: int = 10) -> list[str]:
    tokens = word_tokenize(texto.lower(), language="portuguese")
    tokens = [t for t in tokens if t.isalpha() and t not in STOPWORDS and len(t) > 3]
    mais_comuns = Counter(tokens).most_common(top_n)
    return [palavra for palavra, _ in mais_comuns]


def analisar_log(caminho_arquivo: str) -> dict:
    with open(caminho_arquivo, encoding="utf-8") as f:
        linhas = f.readlines()

    cabecalho = {}
    eventos = []
    texto_completo = ""

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        # Extrai cabecalho (MISSAO:, DATA:, etc.)
        if ":" in linha and not linha.startswith("["):
            chave, _, valor = linha.partition(":")
            if chave.isupper():
                cabecalho[chave.strip()] = valor.strip()
                continue

        texto_completo += " " + linha

        match = REGEX_EVENTO.match(linha)
        if match:
            hora, tag_original, descricao = match.groups()
            severidade = classificar_linha(linha)
            eventos.append({
                "hora": hora,
                "severidade": severidade,
                "descricao": descricao.strip(),
            })

    criticos = [e for e in eventos if e["severidade"] == "CRITICO"]
    alertas  = [e for e in eventos if e["severidade"] == "ALERTA"]

    status_geral = "NORMAL"
    if criticos:
        status_geral = "CRITICO"
    elif alertas:
        status_geral = "ALERTA"

    return {
        "missao": cabecalho.get("MISSAO", "Desconhecida"),
        "data": cabecalho.get("DATA", ""),
        "tripulacao": cabecalho.get("TRIPULACAO", ""),
        "total_eventos": len(eventos),
        "criticos": len(criticos),
        "alertas": len(alertas),
        "status_geral": status_geral,
        "palavras_chave": extrair_palavras_chave(texto_completo),
        "eventos": eventos,
        "detalhes_criticos": [e["descricao"] for e in criticos],
    }
