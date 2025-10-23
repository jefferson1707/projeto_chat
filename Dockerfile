# 1️⃣ Imagem base
FROM python:3.11-slim

# 2️⃣ Define o diretório de trabalho dentro do container
WORKDIR /app

# 3️⃣ Copia o requirements primeiro (para melhor cache)
COPY requirements.txt .

# 4️⃣ Instala dependências do sistema e Python
RUN apt-get update && apt-get install -y build-essential curl \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get remove -y build-essential curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# 5️⃣ Copia o resto da aplicação
COPY . .

# 6️⃣ Cria diretório 'instance' (se necessário)
RUN mkdir -p instance

# 7️⃣ Define variáveis de ambiente do Flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# 8️⃣ Expõe a porta que o Flask vai usar
EXPOSE 5000

# 9️⃣ Comando para rodar a aplicação
CMD ["python", "run.py"]