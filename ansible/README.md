# 🚀 Setup Automático do Ambiente de Desenvolvimento

Este projeto utiliza **Ansible** para automatizar e padronizar a configuração do ambiente de desenvolvimento entre todos os colaboradores.

## 🎯 O Que o Ansible Faz?

Configura automaticamente:
- ✅ **Python 3.11+** e virtualenv
- ✅ **Todas as dependências** do Flask (requirements.txt)
- ✅ **Variáveis de ambiente** (.env)
- ✅ **Sistema de migrações** do banco
- ✅ **Ambiente consistente** entre todos os devs

## 🛠 Pré-requisitos

- **Linux/Ubuntu** ou **WSL** no Windows
- **Git** instalado
- **Python 3.11+** (será instalado automaticamente se necessário)
- Acesso **sudo** para instalação de pacotes do sistema

## 🚀 Setup Rápido (1 Comando)

### Para novos desenvolvedores:
```bash
# 1. Clone o projeto
git clone [URL_DO_REPOSITORIO]
cd projeto_chat

# 2. Execute o setup automático
./setup-dev.sh

# Ou manualmente
ansible-playbook ansible/playbooks/setup-dev.yml --ask-become-pass