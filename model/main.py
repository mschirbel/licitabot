from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import time
import requests

SIM_API_URL = "http://sim-api:8000/similarity"
app = FastAPI()
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

class Texts(BaseModel):
    text1: str
    text2: str




@app.post("/similarity")
def compute_similarity(data: Texts):
    embeddings = model.encode([data.text1, data.text2])
    score = util.cos_sim(embeddings[0], embeddings[1]).item()
    return {"similarity_score": round(score, 4)}

@app.get("/health")
def healthcheck():
    print("⏳ Aguardando modelo ficar disponível...")
    inicio = time.time()
    while True:
        try:
            r = requests.post(SIM_API_URL, json={"text1": "teste", "text2": "teste"}, timeout=5)
            if r.status_code == 200:
                print("✅ Modelo pronto!\n")
                break
        except requests.exceptions.RequestException:
            pass

        if time.time() - inicio > 300:
            print("❌ Timeout: modelo não respondeu dentro do tempo limite.")
            exit(1)

        time.sleep(2)