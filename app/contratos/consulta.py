import requests
from config import BASE_URL, START_FMT, END_FMT
from similarity.sim import calcular_similaridade

def buscar_contratos(texto_empresa):
    pagina = 1
    tamanho_pagina = 100

    while True:
        params = {
            "dataInicial": START_FMT,
            "dataFinal": END_FMT,
            "pagina": pagina,
            "tamanhoPagina": tamanho_pagina
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"❌ Erro ao buscar contratos: {e}")
            break

        contratos = data.get("contratos") or data.get("data") or []
        if not contratos:
            break

        for contrato in contratos:
            objeto = contrato.get("objetoContrato", "")
            if not objeto:
                continue

            score = calcular_similaridade(objeto, texto_empresa)
            print(type(score))
            numero = contrato.get("numeroContratoEmpenho", "N/A")
            orgao = contrato.get("orgaoEntidade", {}).get("razaoSocial", "N/A")
            municipio = contrato.get("unidadeOrgao", {}).get("municipioNome", "N/A")
            uf = contrato.get("unidadeOrgao", {}).get("ufSigla", "N/A")
            data_inicio = contrato.get("dataVigenciaInicio", "N/A")
            data_fim = contrato.get("dataVigenciaFim", "N/A")
            valor = contrato.get("valorInicial", "N/A")
            modalidade = contrato.get("categoriaProcesso", {}).get("nome", "N/A")

            print(f"📄 Contrato: {numero}")
            print(f"🏢 Órgão: {orgao} - {municipio}/{uf}")
            print(f"📦 Modalidade: {modalidade}")
            print(f"💬 Objeto: {objeto}")
            print(f"💰 Valor: {valor} | 🗓 {data_inicio} → {data_fim}")
            print(f"🧠 Score de similaridade: {score}")
            print("\n" + "="*80 + "\n")

        if len(contratos) < tamanho_pagina:
            break
        pagina += 1
