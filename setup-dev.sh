#!/bin/bash
# setup-dev.sh

echo "🚀 Configurando ambiente de desenvolvimento Flask..."

# Verificar se Ansible está instalado
if ! command -v ansible-playbook &> /dev/null; then
    echo "📦 Instalando Ansible..."
    sudo apt update
    sudo apt install -y ansible
fi

# Executar playbook
echo "🐍 Executando configuração com Ansible..."
ansible-playbook ansible/playbooks/setup-dev.yml

echo "✅ Configuração concluída!"
echo ""
echo "📝 Próximos passos:"
echo "1. Adicione sua GEMINI_API_KEY no arquivo .env"
echo "2. Ative o ambiente virtual: source venv/bin/activate"
echo "3. Execute a aplicação: flask run"
echo ""
echo "🌐 A aplicação estará disponível em: http://localhost:5000"
