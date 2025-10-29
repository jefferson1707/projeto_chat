# 🚀 Infraestrutura como Código - Render

Este diretório contém a configuração Terraform para provisionar e gerenciar a infraestrutura do projeto no [Render](https://render.com).

## 📋 Pré-requisitos

- [Terraform](https://developer.hashicorp.com/terraform/downloads) >= 1.0
- Conta no [Render](https://render.com)
- Chave de API do Render

## 🔑 Configuração Inicial

### 1. Configurar Variáveis de Ambiente
```bash
# Obtenha sua API Key em: https://dashboard.render.com/account/api-keys
export RENDER_API_KEY="sua_api_key_aqui"

# Obtenha seu Owner ID em: https://dashboard.render.com/account/settings
export RENDER_OWNER_ID="seu_owner_id_aqui"