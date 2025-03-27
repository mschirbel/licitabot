import requests
from datetime import datetime
import json
import spacy
import nltk
from nltk.corpus import stopwords

# Baixar stopwords se necessário
nltk.download('stopwords')

# spaCy pt-BR
nlp = spacy.load("pt_core_news_sm")
stopwords_pt = set(stopwords.words("portuguese"))

# Carregar dados da empresa
with open("empresa.json", encoding="utf-8") as f:
    empresa = json.load(f)
empresa_keywords = {kw.lower() for kw in empresa["fornecedor"]["procurementInterests"]}

# Datas da busca
start_date = "2024-01-01"
end_date = "2024-01-31"
start_fmt = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y%m%d")
end_fmt = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y%m%d")

# API
BASE_URL = "https://pncp.gov.br/api/consulta/v1/contratos"
pagina = 1
tamanho_pagina = 100

print(f"🔍 Buscando licitações entre {start_date} e {end_date}...\n")

# Função para calcular score
def calcular_score_match(licitacao_objeto, empresa_keywords):
    doc = nlp(licitacao_objeto)
    lic_keywords = {token.lemma_.lower() for token in doc if token.pos_ == "NOUN" and token.text.lower() not in stopwords_pt}

    if not lic_keywords:
        return 0.0, set(), set() 

    intersecao = lic_keywords & empresa_keywords
    score = len(intersecao) / len(lic_keywords)
    return round(score * 10, 2), lic_keywords, intersecao

# Loop da API
while True:
    params = {
        "dataInicial": start_fmt,
        "dataFinal": end_fmt,
        "pagina": pagina,
        "tamanhoPagina": tamanho_pagina
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ Erro ao buscar dados: {e}")
        break

    contratos = data.get("contratos") or data.get("data") or []
    if not contratos:
        print("⚠️ Nenhum contrato encontrado.")
        break

    for contrato in contratos:
        objeto = contrato.get("objetoContrato", "N/A")
        numero = contrato.get("numeroContratoEmpenho", "N/A")
        orgao = contrato.get("orgaoEntidade", {}).get("razaoSocial", "N/A")
        municipio = contrato.get("unidadeOrgao", {}).get("municipioNome", "N/A")
        uf = contrato.get("unidadeOrgao", {}).get("ufSigla", "N/A")
        data_inicio = contrato.get("dataVigenciaInicio", "N/A")
        data_fim = contrato.get("dataVigenciaFim", "N/A")
        valor = contrato.get("valorInicial", "N/A")

        score, lic_keywords, intersecao = calcular_score_match(objeto, empresa_keywords)

        print(f"📄 Contrato: {numero}")
        print(f"🏢 Órgão: {orgao} - {municipio}/{uf}")
        print(f"💬 Objeto: {objeto}")
        print(f"💰 Valor: {valor} | 🗓 {data_inicio} → {data_fim}")
        print(f"🧠 Score de compatibilidade: {score}/10")
        print(f"🔑 Palavras-chave da licitação: {sorted(lic_keywords)}")
        print(f"✅ Match com empresa: {sorted(intersecao)}\n")

    if len(contratos) < tamanho_pagina:
        break
    pagina += 1
