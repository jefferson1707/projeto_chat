# parte 6: esta parte foi deixada para a parte 4, para podermmpos testar ao decorrer do desenvolvimento

# Vamos importar o app
from app import create_app

# step 1: cria aplicação flask
app = create_app()

# step 2: roda o app
if __name__ == "__main__":
    # executando aplicação em modo desenvolvimento
    app.run(debug=True)
