# Parte 4

# Este arquivo faz a pasta 'routes' ser um módulo Python
# Pode ficar vazio ou ter imports comuns

from flask import Blueprint, render_template

# Step 1: cria o blueprint home
# Esplicação: __name__ ajuda o flask a encontrar templates
home_bp = Blueprint("home", __name__)


# Step 2: rota para a pagina incial
@home_bp.route("/")
def index():
    return render_template("index.html")
