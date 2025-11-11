# 1. Imagem base: Começamos com uma imagem oficial do Python
FROM python:3.10-slim

# 2. Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --- NOVO PASSO ---
# 3. Instala as dependências de sistema (especificamente libgomp1 para o PyCaret)
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*
# --- FIM DO NOVO PASSO ---

# 4. Cria o diretório de trabalho dentro do contêiner
WORKDIR /app

# 5. Copia a lista de dependências
COPY requirements.txt /app/

# 6. Instala as dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 7. Copia o resto do código do projeto para dentro do contêiner
COPY . /app/