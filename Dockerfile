# Base com Python 3.10
FROM python:3.10-slim

# Variáveis de ambiente para evitar prompts do spaCy
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório de trabalho
WORKDIR /app

# Copia os arquivos
COPY requirements.txt .

# Instala dependências Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Baixa o modelo do spaCy para português
RUN python -m spacy download pt_core_news_sm

# Copia os arquivos
COPY licitacao.py .
COPY empresa.json .

CMD ["python", "licitacao.py"]
