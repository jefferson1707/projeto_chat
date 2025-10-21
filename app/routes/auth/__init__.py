# Parte 10: este arquivo faz a pasta 'routes' ser um pacote Python

# Importa blueprints de auth para organização
from app.routes.auth.login import auth_bp
from app.routes.auth.minha_conta import minha_conta_bp

__all__ = ['auth_bp', 'minha_conta_bp']