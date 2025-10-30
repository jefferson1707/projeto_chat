FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema (incluindo sqlite3)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements primeiro para cache
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia a aplicação
COPY . .

# Cria diretório instance com permissões
RUN mkdir -p instance && chmod 755 instance

# Porta que o Render usa
ENV PORT=10000
EXPOSE 10000

# Health check para o Render
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:10000/ || exit 1

# Comando para rodar (Render usa PORT automático)
CMD exec gunicorn --bind 0.0.0.0:$PORT run:app