FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema (necessárias para spaCy)
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos para o container
COPY requirements.txt .

# Instala dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia os arquivos para o container
COPY . .

# ENTRYPOINT define o comando principal da app
ENTRYPOINT ["python", "main.py"]
