terraform {
  required_providers {
    render = {
      source  = "render-oss/render"
      version = "0.2.0"
    }
  }
  required_version = ">= 1.5.0"
}

# PROVIDER CONFIGURATION (ADICIONE ESTE BLOCO)
provider "render" {
  api_key  = var.render_api_key
  owner_id = var.render_owner_id
}

resource "render_web_service" "projeto_chat" {
  name    = "projeto-chat"
  plan    = "starter"
  region  = "oregon"

  # Configuração obrigatória do runtime_source
  runtime_source = {
    docker = {
      repo_url        = "https://github.com/jefferson1707/projeto_chat"
      branch          = "main"
      dockerfile_path = "Dockerfile"
      auto_deploy     = true
    }
  }

  
  env_vars = {
    GEMINI_API_KEY = {
      value = var.gemini_api_key
    }
    SQLALCHEMY_DATABASE_URI = {
      value = "sqlite:////tmp/chat.db"
    }
    FLASK_ENV = {
      value = "production"
    }
    PORT = {
      value = "10000"
    }
    SECRET_KEY = {
      value = var.flask_secret_key
    }
  }

  # Comando de start (opcional, mas recomendado)
  start_command = "python run.py"

  # Configurações opcionais
  health_check_path = "/"  
  num_instances     = 1
}