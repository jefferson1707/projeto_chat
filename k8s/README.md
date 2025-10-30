 Arquivos de Configuração
🚀 deployment.yml - Configuração Principal do Deployment
Função: Gerencia o ciclo de vida dos pods e containers da aplicação.

Configurações Detalhadas:

Réplicas: 2 instâncias da aplicação para alta disponibilidade

Imagem: jefferson1707/projeto_chat:latest - Imagem Docker da aplicação

Porta: Container exposto na porta 5000

Recursos Computacionais:

Requests: 256Mi Memory, 100m CPU

Limits: 512Mi Memory, 200m CPU

Health Checks:

Liveness Probe: Verifica saúde da aplicação (inicia após 30s, verifica a cada 10s)

Readiness Probe: Verifica prontidão para tráfego (inicia após 5s, verifica a cada 5s)

Volumes: Volume emptyDir montado em /app/instance para persistência do SQLite

Variáveis de Ambiente:

PORT: 5000

FLASK_ENV: production

DEBUG: false

SQLALCHEMY_DATABASE_URI: sqlite:////app/instance/chat.db

SECRET_KEY e GEMINI_API_KEY: Obtidos via Kubernetes Secrets

🌐 service.yml - Configuração do Service
Função: Fornece um ponto de acesso estável e balanceamento de carga para os pods.

Configurações:

Tipo: LoadBalancer - Distribui tráfego entre as réplicas e pode provisionar um IP externo

Port Mapping: Porta 80 externa → Porta 5000 do container

Selector: Conecta ao deployment através do label app: projeto-chat

Protocolo: TCP para comunicação

🛣️ ingress.yml - Configuração do Ingress
Função: Gerencia roteamento de tráfego HTTP/HTTPS e regras de acesso.

Configurações:

Ingress Class: nginx - Controlador de Ingress utilizado

Rota: / com PathType Prefix direcionado para o service

Backend: Aponta para projeto-chat-service na porta 80

Annotations: Configurações específicas para o ingress controller

🔐 secret-template.yml - Template de Secrets
⚠️ ARQUIVO SENSÍVEL - NÃO DEVE SER COMMITADO

Função: Armazenar dados sensíveis de forma segura no cluster Kubernetes.

Dados Configurados:

secret-key: Chave secreta para a aplicação Flask (sessões, CSRF protection)

gemini-api-key: Chave da API Gemini para funcionalidades de IA do chat

🚨 IMPORTANTE:

Este arquivo serve como template

Deve ser copiado para secrets.yml com valores reais

Nunca commitar com chaves reais no repositório

Aplicar com: kubectl apply -f secrets.yml

⚙️ configMap-prod.yml - ConfigMap para Produção
Função: Configurações não sensíveis para ambiente de produção.

Configurações:

flask_env: "production" - Ambiente Flask

debug: "false" - Modo debug desativado

database_uri: "sqlite:////app/instance/chat.db" - Database de produção

🛠️ configmap-dev.yml - ConfigMap para Desenvolvimento
Função: Configurações específicas para ambiente de desenvolvimento.

Configurações:

flask_env: "development" - Ambiente de desenvolvimento

debug: "true" - Modo debug ativado para troubleshooting

database_uri: "sqlite:////app/instance/chat-dev.db" - Database separado para dev

🛠️ Como Usar - Fluxo Completo
1. 🔒 Configurar Secrets (Primeira Vez)
bash
# Copiar template e editar com valores reais
cp secret-template.yml secrets.yml
nano secrets.yml

# Aplicar secrets no cluster
kubectl apply -f secrets.yml
2. 📦 Implantar a Aplicação
bash
# Aplicar todos os recursos (em ordem recomendada)
kubectl apply -f configMap-prod.yml       # Configurações
kubectl apply -f deployment.yml          # Aplicação principal
kubectl apply -f service.yml             # Service
kubectl apply -f ingress.yml             # Ingress (se necessário)
3. ✅ Verificar e Monitorar
bash
# Verificar status geral
kubectl get all -l app=projeto-chat

# Verificar pods específicos
kubectl get pods -l app=projeto-chat

# Verificar logs da aplicação
kubectl logs -l app=projeto-chat --tail=50

# Verificar serviços e ingress
kubectl get svc,ingress

# Verificar eventos do cluster
kubectl get events --sort-by=.metadata.creationTimestamp
🔧 Estrutura do .gitignore Recomendada
text
# Kubernetes Secrets - NUNCA COMMITAR
secret-template.yml
secrets.yml
*-secrets.yml
*-secret.yml
secrets/

# Configurações de ambiente (opcional)
configmap-dev.yml
configMap-prod.yml

# Arquivos do Kubernetes
kubeconfig
.kube/
*.tmp
🆘 Troubleshooting e Comandos Úteis
Diagnóstico
bash
# Descrever recursos para detalhes
kubectl describe deployment projeto-chat
kubectl describe service projeto-chat-service
kubectl describe pod -l app=projeto-chat

# Verificar configurações aplicadas
kubectl get configmaps
kubectl get secrets

# Acessar shell dentro do pod
kubectl exec -it <pod-name> -- /bin/bash
Gerenciamento
bash
# Recriar deployment específico
kubectl rollout restart deployment/projeto-chat

# Escalar réplicas
kubectl scale deployment/projeto-chat --replicas=3

# Deletar e recriar tudo
kubectl delete -f .
kubectl apply -f .
Logs e Monitoramento
bash
# Seguir logs em tempo real
kubectl logs -l app=projeto-chat -f

# Logs de um pod específico
kubectl logs <pod-name>

# Verificar recursos consumidos
kubectl top pods -l app=projeto-chat
📊 Arquitetura Implantada
text
┌─────────────────┐    ┌──────────────────┐    ┌────────────────┐
│   Ingress       │    │   Service        │    │   Deployment   │
│   (ingress.yml) │───▶│   (service.yml)  │───▶│   (deployment. │
│                 │    │   LoadBalancer   │    │   yml)         │
└─────────────────┘    └──────────────────┘    └────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌────────────────┐
│   ConfigMap     │    │   Secrets        │    │   Pods (2x)    │
│   (configMap-   │    │   (secrets.yml)  │    │   - App        │
│   prod.yml)     │    │                  │    │   - Volume     │
└─────────────────┘    └──────────────────┘    └────────────────┘