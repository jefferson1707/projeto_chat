#!/bin/bash
echo "🚀 Deploying to Render Kubernetes..."

# Aplicar configurações
kubectl apply -f k8s/configmap-prod.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

echo "Deploy completed!"
echo "Your app will be available at: https://projeto-chat.onrender.com"