# parte 6: esta parte foi deixada para a parte 4, para podermmpos testar ao decorrer do desenvolvimento

# Vamos importar o app
from app import create_app, db
import os

# step 1: cria aplicação flask
app = create_app()

# Step 2: cria o banco de dados para o docker 
with app.app_context():
    db.create_all()

# step 3: roda o app
if __name__ == "__main__":

    # Step 3.1: desenvolvimento: debug ativado
    # debug desativado (usar variável de ambiente)
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'

    # Step 3.2: define porta de execução dinâmica (Render define PORT)
    port = int(os.environ.get("PORT", 5000))

    # step 3.3: executando aplicação em modo desenvolvimento, debug ativado,
    #  host 0.0.0.0 e porta 5000 para sincronizar com o docker
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
