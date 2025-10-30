# Funcionamento do ci/cd


graph TD
    A[Push para main] --> B[CI: Testes e Validação]
    B --> C{Testes Passaram?}
    C -->|Sim| D[CD: Build Docker]
    C -->|Não| E[Falha - Notificação]
    D --> F[Push para Docker Hub]
    F --> G[✅ Deploy Pronto]


 # Para debug local do Dockerfile:
docker build -t teste .
docker run -p 5000:5000 teste   