import json
import os

def carregar_texto_empresa(caminho=None):
    if caminho is None:
        caminho = os.path.join(os.path.dirname(__file__), "empresas.json")

    with open(caminho, encoding="utf-8") as f:
        empresa = json.load(f)

    return " ".join([
        empresa.get("segmento_principal", ""),
        empresa.get("produtos_oferecidos", ""),
        empresa.get("detalhes_produtos_servicos", "")
    ])
