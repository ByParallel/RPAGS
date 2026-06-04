"""
Modulo de Visao Computacional - Analise de imagens de sensores espaciais.
Detecta anomalias, classifica brilho e identifica padroes.
"""
import cv2
import numpy as np
from PIL import Image


def carregar_imagem(caminho: str) -> np.ndarray:
    img = cv2.imread(caminho)
    if img is None:
        raise FileNotFoundError(f"Imagem nao encontrada: {caminho}")
    return img


def analisar_brilho(img_gray: np.ndarray) -> dict:
    media = float(np.mean(img_gray))
    desvio = float(np.std(img_gray))
    minimo = int(np.min(img_gray))
    maximo = int(np.max(img_gray))
    return {"media": round(media, 2), "desvio": round(desvio, 2),
            "minimo": minimo, "maximo": maximo}


def detectar_regioes_anomalas(img_gray: np.ndarray, limiar: int = 180) -> dict:
    """Detecta regioes com brilho anomalo (muito alto = possivel anomalia termica)."""
    _, mask = cv2.threshold(img_gray, limiar, 255, cv2.THRESH_BINARY)
    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total_pixels = img_gray.size
    pixels_anomalos = int(np.sum(mask > 0))
    percentual = round(pixels_anomalos / total_pixels * 100, 2)
    return {
        "regioes_anomalas": len(contornos),
        "percentual_area_anomala": percentual,
        "anomalia_detectada": percentual > 2.0,
    }


def calcular_contraste(img_gray: np.ndarray) -> float:
    """Calcula o contraste via desvio padrao (metrica simples e eficaz)."""
    return round(float(np.std(img_gray)), 2)


def classificar_imagem(brilho: dict, anomalia: dict, contraste: float) -> str:
    if anomalia["anomalia_detectada"] and brilho["media"] > 120:
        return "ANOMALIA TERMICA"
    if anomalia["anomalia_detectada"]:
        return "ANOMALIA DETECTADA"
    if contraste > 60:
        return "ALTO CONTRASTE (possivel cratera/pluma)"
    if brilho["media"] < 50:
        return "SUPERFICIE ESCURA (normal)"
    return "SUPERFICIE NORMAL"


def analisar_imagem(caminho: str) -> dict:
    img = carregar_imagem(caminho)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    brilho = analisar_brilho(img_gray)
    anomalia = detectar_regioes_anomalas(img_gray)
    contraste = calcular_contraste(img_gray)
    classificacao = classificar_imagem(brilho, anomalia, contraste)

    # Histograma simplificado (3 faixas: escuro / medio / brilhante)
    total = img_gray.size
    escuro    = int(np.sum(img_gray < 85))
    medio     = int(np.sum((img_gray >= 85) & (img_gray < 170)))
    brilhante = int(np.sum(img_gray >= 170))

    return {
        "arquivo": caminho.split("\\")[-1].split("/")[-1],
        "resolucao": f"{img.shape[1]}x{img.shape[0]}",
        "brilho_medio": brilho["media"],
        "desvio_padrao": brilho["desvio"],
        "contraste": contraste,
        "regioes_anomalas": anomalia["regioes_anomalas"],
        "percentual_anomalo": anomalia["percentual_area_anomala"],
        "anomalia_detectada": anomalia["anomalia_detectada"],
        "classificacao": classificacao,
        "pixels_escuros_pct": round(escuro / total * 100, 1),
        "pixels_medios_pct": round(medio / total * 100, 1),
        "pixels_brilhantes_pct": round(brilhante / total * 100, 1),
    }
