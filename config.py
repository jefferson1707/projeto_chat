# parte 2: conexão entre o .env e banco de dados
import os # Interface com o sistema operacional - acessa variáveis de ambiente, arquivos, etc.
from dotenv import load_dotenv  # Carrega variáveis de ambiente do arquivo .env para o sistema


# Step 1: carrega as variaveis do arquivo .env
load_dotenv()

# step 2: vammos usar classe por questa de performace, para comfigurações fixas e organização.
class Config:

    # step 2.1: configurações de segurança
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Step 2.2: configurações de banco de dados
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Step 2.3: configuração de debug
    DEBUG = os.getenv("DEBUG")