#  Parte 3

from config import Config # importando o arquivo config.py
from flask import Flask  # Framework web principal - cria a aplicação Flask
from flask_login import \
    LoginManager  # Gerenciamento de sessões de usuário - autenticação, login, logout
from flask_migrate import \
    Migrate  # Sistema de migrações - para versionar e atualizar o esquema do banco
from flask_sqlalchemy import \
    SQLAlchemy  # ORM - para trabalhar com banco de dados usando Python
from flask_bcrypt import \
    Bcrypt  # Criptografia de senha
from flask_cors import \
      CORS # Permite que o front-end acesse o back-end em todos os navegadores


# Step 1: cria as instancias
db = SQLAlchemy()  # para banco de dados
migrate = Migrate()  # para migrations do banco de dados
login_manager = LoginManager()  # para gerenciar logins
bcrypt = Bcrypt()   # para criptografia

# step 2: cria o app
def create_app():

    # Step 2.1: aqui criamos a instancia do flask e atribuimos ao cors
    app = Flask(__name__)
    CORS(app)

    # Step 2.2: pegados do arquivo .env
    app.config.from_object(Config) # Espera uma class do config.py

    # Step 2.3: se o arquivo não for encontrado, ele emite uma mensagem de erro
    if not app.config["SECRET_KEY"]:
        raise ValueError(
            "Voce precisa criar um arquivo .env com uma chave segura para o SECRET_KEY"
        )

    # Step 2.4: tribui as variaveis das instancias
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(
        app
    )  # Explicação: diz ao login_manager qual app ele vai gerenciar
    bcrypt.init_app(app) 

    # Step 2.5: configurações do LoginManager
    login_manager.login_view = (
        "auth.login"  # explicação: Onde mandar usuários não logados
    )
    login_manager.login_message = "Voce precisa estar logado para acessar essa pagina"

    # Step 2.6: Importar e registrar os blueprints (rotas)
    # explicação: importante essas importações estarem dentro da Função
    # para evitar erros de circulação de importe
    from app.routes import home_bp, auth_bp, minha_conta_bp, sobre_bp

    # Step 2.7: registra os blueprints
    app.register_blueprint(home_bp)  # Pagina inicial deve ser direta e sem prefixo
    app.register_blueprint(auth_bp, url_prefix="/auth")  # Prefixo para todas as rota
    app.register_blueprint(minha_conta_bp, url_prefix='/minha-conta') 
    app.register_blueprint(sobre_bp)

    return app
