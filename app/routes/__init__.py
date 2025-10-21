# Parte 11:

# Importa todos os blueprints para facilitar imports em outros lugares
from app.routes.home import home_bp
from app.routes.auth.login import auth_bp
from app.routes.auth.minha_conta import minha_conta_bp
from app.routes.sobre import sobre_bp

__all__ = ['home_bp', 'auth_bp', 'minha_conta_bp', 'sobre_bp']