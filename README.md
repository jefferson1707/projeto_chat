# Projeto_chat: read_me em desenvolvimento ainda

Para usar:

git clone seu-repositorio
docker build -t projeto_chat .
docker run -p 5000:5000 projeto_chat

Para mudanças no codigo:

Rebuild da imagem
docker build -t projeto_chat .

Recriar container
docker rm -f chat_app
docker run -d --name chat_app -p 5000:5000 --env-file .env projeto_chat
