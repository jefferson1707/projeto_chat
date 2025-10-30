#!/bin/bash
echo "🔧 Deploying to local Kubernetes..."

# Criar secrets a partir do template (desenvolvimento)
kubectl create secret generic projeto-chat-secrets \
  --from-literal=secret-key="dev-secret-key-123" \
  --from-literal=gemini-api-key="dev-gemini-key-456" \
  --dry-run=client -o yaml > k8s/secret-dev.yaml

# Aplicar configurações
kubectl apply -f k8s/configmap-dev.yaml
kubectl apply -f k8s/secret-dev.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

echo "✅ Local deploy completed!"
echo "🌐 Access your app: kubectl port-forward svc/projeto-chat-service 8080:80"