# teste:

import os
import sys
from app import create_app, db

def test_app_creation():
    """Testa se a aplicação Flask cria corretamente"""
    print("🔧 Testando criação da aplicação...")
    try:
        app = create_app()
        with app.app_context():
            db.create_all()  # Cria tabelas se não existirem
        print(" Aplicação criada com sucesso!")
        return True
    except Exception as e:
        print(f" Erro ao criar aplicação: {e}")
        return False

def test_database_connection():
    """Testa conexão com o banco de dados"""
    print(" Testando conexão com banco...")
    try:
        app = create_app()
        with app.app_context():
            # Tenta uma query simples
            from app.models import User
            users = User.query.limit(1).all()
        print(" Conexão com banco funcionando!")
        return True
    except Exception as e:
        print(f"Erro no banco: {e}")
        return False

def test_routes():
    """Testa se as rotas básicas funcionam"""
    print(" Testando rotas...")
    try:
        app = create_app()
        with app.test_client() as client:
            # Testa rota home
            response = client.get('/')
            assert response.status_code in [200, 302]  # 200 OK ou 302 Redirect
            print(" Rota / funcionando!")
            
            # Testa rota login
            response = client.get('/auth/login')
            assert response.status_code == 200
            print("Rota /auth/login funcionando!")
            
    except Exception as e:
        print(f" Erro nas rotas: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print(" Iniciando testes da aplicação...")
    print("=" * 50)
    
    tests = [
        test_app_creation,
        test_database_connection, 
        test_routes
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f" Resultado: {passed}/{len(tests)} testes passaram")
    
    if passed == len(tests):
        print(" Todos os testes passaram! Aplicação pronta.")
    else:
        print(" Alguns testes falharam. Verifique os erros acima.")