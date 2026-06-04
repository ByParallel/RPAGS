"""
Script auxiliar para gerar imagens de sensor simuladas para teste.
Execute uma vez antes do main.py se nao tiver imagens proprias.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = "data/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

rng = np.random.default_rng(42)


def gerar_imagem_superfície_lunar(nome, anomalia=False):
    arr = rng.integers(30, 80, (256, 256), dtype=np.uint8)
    if anomalia:
        arr[100:150, 100:150] = rng.integers(200, 255, (50, 50), dtype=np.uint8)
    img = Image.fromarray(arr, mode="L").convert("RGB")
    draw = ImageDraw.Draw(img)
    label = "ANOMALIA DETECTADA" if anomalia else "SUPERFICIE NORMAL"
    draw.text((5, 5), label, fill=(255, 255, 0))
    img.save(os.path.join(OUTPUT_DIR, nome))
    print(f"  Gerada: {nome}")


def gerar_imagem_pluma(nome):
    arr = rng.integers(10, 40, (256, 256), dtype=np.uint8)
    # pluma brilhante no centro
    for i in range(256):
        for j in range(256):
            dist = ((i - 128) ** 2 + (j - 128) ** 2) ** 0.5
            if dist < 40:
                arr[i, j] = min(255, arr[i, j] + int((40 - dist) * 4))
    img = Image.fromarray(arr, mode="L").convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.text((5, 5), "PLUMA DE VAPOR", fill=(0, 255, 255))
    img.save(os.path.join(OUTPUT_DIR, nome))
    print(f"  Gerada: {nome}")


def gerar_imagem_cratera(nome):
    arr = rng.integers(50, 100, (256, 256), dtype=np.uint8)
    # anel escuro de cratera
    for i in range(256):
        for j in range(256):
            dist = abs(((i - 128) ** 2 + (j - 128) ** 2) ** 0.5 - 60)
            if dist < 10:
                arr[i, j] = np.uint8(max(0, int(arr[i, j]) - int((10 - dist) * 8)))
    img = Image.fromarray(arr, mode="L").convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.text((5, 5), "CRATERA LUNAR", fill=(255, 128, 0))
    img.save(os.path.join(OUTPUT_DIR, nome))
    print(f"  Gerada: {nome}")


if __name__ == "__main__":
    print("Gerando imagens de sensor simuladas...")
    gerar_imagem_superfície_lunar("artemis01_sensor_001.png", anomalia=False)
    gerar_imagem_superfície_lunar("artemis01_sensor_002.png", anomalia=True)
    gerar_imagem_superfície_lunar("artemis02_sensor_001.png", anomalia=False)
    gerar_imagem_pluma("europa03_sensor_001.png")
    gerar_imagem_cratera("artemis02_sensor_002.png")
    gerar_imagem_superfície_lunar("europa03_sensor_002.png", anomalia=True)
    print("Imagens geradas com sucesso em data/images/")
