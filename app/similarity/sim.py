import requests
from config import SIM_API_URL

def calcular_similaridade(text1, text2):
    try:
        response = requests.post(SIM_API_URL, json={"text1": text1, "text2": text2})
        response.raise_for_status()
        return response.json().get("similarity_score", 0.0)
    except Exception as e:
        print(f"⚠️ Erro ao calcular similaridade: {e}")
        return 0.0
