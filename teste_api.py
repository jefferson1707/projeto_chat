# debug_gemini_25_flash.py
import google.generativeai as genai
import time
from datetime import datetime

def debug_gemini_25_flash():
    """
    Debug específico para o modelo gemini-2.5-flash
    """
    API_KEY = "minha chave api"
    
    print("🚀 DEBUG ESPECÍFICO - GEMINI 2.5 FLASH")
    print("=" * 60)
    print(f"📅 Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔑 Chave: {API_KEY[:10]}...{API_KEY[-4:]}")
    print(f"🤖 Modelo: gemini-2.5-flash")
    print("=" * 60)
    
    try:
        # 1. Configurar API
        print("\n1️⃣  CONFIGURANDO API...")
        genai.configure(api_key=API_KEY)
        print("✅ API configurada com sucesso")
        
        # 2. Verificar se o modelo está disponível
        print("\n2️⃣  VERIFICANDO DISPONIBILIDADE DO MODELO...")
        modelos = list(genai.list_models())
        modelo_25_flash = None
        
        for model in modelos:
            if "gemini-2.5-flash" in model.name:
                modelo_25_flash = model
                break
        
        if modelo_25_flash:
            print("✅ Modelo gemini-2.5-flash encontrado!")
            print(f"   📝 Nome completo: {modelo_25_flash.name}")
            print(f"   📋 Display Name: {modelo_25_flash.display_name}")
            print(f"   📖 Descrição: {modelo_25_flash.description}")
            print(f"   🔢 Input Tokens: {modelo_25_flash.input_token_limit}")
            print(f"   🔢 Output Tokens: {modelo_25_flash.output_token_limit}")
        else:
            print("❌ Modelo gemini-2.5-flash não encontrado na lista")
            print("   📋 Modelos disponíveis:")
            for model in modelos[:5]:  # Mostra apenas os primeiros 5
                if "gemini" in model.name.lower():
                    print(f"     - {model.name}")
            return False
        
        # 3. Inicializar o modelo específico
        print("\n3️⃣  INICIALIZANDO MODELO...")
        model = genai.GenerativeModel("gemini-2.5-flash")
        print("✅ Modelo inicializado com sucesso")
        
        # 4. Teste de contagem de tokens
        print("\n4️⃣  TESTANDO CONTAGEM DE TOKENS...")
        try:
            texto_teste = "Teste de contagem de tokens para gemini-2.5-flash"
            token_count = model.count_tokens(texto_teste)
            print(f"✅ Contagem de tokens funcionando:")
            print(f"   Texto: '{texto_teste}'")
            print(f"   Total de tokens: {token_count.total_tokens}")
        except Exception as e:
            print(f"❌ Erro na contagem de tokens: {e}")
        
        # 5. Teste de geração de conteúdo
        print("\n5️⃣  TESTANDO GERAÇÃO DE CONTEÚDO...")
        
        # Primeira tentativa
        try:
            start_time = time.time()
            response = model.generate_content(
                "Responda brevemente: Qual é a capital do Brasil?"
            )
            end_time = time.time()
            
            print(f"✅ Geração bem-sucedida!")
            print(f"   Resposta: {response.text}")
            print(f"   Tempo de resposta: {(end_time - start_time):.2f}s")
            
            # Verificar metadados da resposta
            if hasattr(response, 'usage_metadata'):
                print(f"   📊 Usage: {response.usage_metadata}")
                
        except Exception as e:
            error_str = str(e)
            print(f"❌ Erro na geração: {error_str}")
            
            # Tratamento específico para erro 429
            if "429" in error_str and "quota" in error_str.lower():
                print("\n💡 INFORMAÇÕES SOBRE COTA:")
                print("   - Cota gratuita esgotada para este modelo")
                print("   - Soluções possíveis:")
                print("     1. Aguardar até o próximo ciclo mensal")
                print("     2. Configurar faturamento no Google AI Studio")
                print("     3. Usar outro modelo (gemini-1.5-flash)")
                print("     4. Criar nova conta Google")
                
                # Tentar extrair tempo de espera
                if "retry in" in error_str:
                    import re
                    match = re.search(r"retry in ([\d.]+)s", error_str)
                    if match:
                        wait_time = float(match.group(1))
                        print(f"   ⏰ Sugere aguardar: {wait_time} segundos")
                return False
        
        # 6. Teste com configurações personalizadas
        print("\n6️⃣  TESTANDO CONFIGURAÇÕES PERSONALIZADAS...")
        try:
            generation_config = {
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 100,
            }
            
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
            
            response = model.generate_content(
                "Explique em uma frase: inteligência artificial",
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            print(f"✅ Configurações personalizadas funcionando:")
            print(f"   Resposta: {response.text}")
            
        except Exception as e:
            print(f"⚠️  Erro nas configurações personalizadas: {e}")
        
        # 7. Teste de performance
        print("\n7️⃣  TESTE DE PERFORMANCE...")
        try:
            tempos = []
            for i in range(2):  # 2 requisições rápidas
                start_time = time.time()
                response = model.generate_content(f"Teste de performance {i+1}")
                end_time = time.time()
                tempo_resposta = end_time - start_time
                tempos.append(tempo_resposta)
                
                print(f"   ✅ Requisição {i+1}: {tempo_resposta:.2f}s - {len(response.text)} chars")
            
            tempo_medio = sum(tempos) / len(tempos)
            print(f"   📊 Tempo médio: {tempo_medio:.2f}s")
            
        except Exception as e:
            print(f"❌ Erro no teste de performance: {e}")
        
        # 8. Teste com contexto
        print("\n8️⃣  TESTANDO CHAT COM CONTEXTO...")
        try:
            chat = model.start_chat(history=[])
            
            # Primeira mensagem
            response1 = chat.send_message("Meu nome é João.")
            print(f"   📝 Resposta 1: {response1.text}")
            
            # Segunda mensagem com contexto
            response2 = chat.send_message("Qual é o meu nome?")
            print(f"   📝 Resposta 2: {response2.text}")
            
            print("✅ Chat com contexto funcionando!")
            
        except Exception as e:
            print(f"❌ Erro no chat com contexto: {e}")
        
        print("\n" + "=" * 60)
        print("🎉 DEBUG DO GEMINI-2.5-FLASH CONCLUÍDO!")
        print("✅ A chave e o modelo estão configurados corretamente")
        print("📋 Próximos passos:")
        print("   1. Implemente o tratamento de erros 429")
        print("   2. Configure rate limiting adequado")
        print("   3. Use este modelo em sua aplicação")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        print("💡 Possíveis causas:")
        print("   - Chave API inválida ou revogada")
        print("   - Modelo não disponível na região")
        print("   - Problemas de conexão com a internet")
        return False

def verificar_alternativas():
    """
    Verifica modelos alternativos caso o 2.5-flash não funcione
    """
    print("\n" + "🔄 VERIFICANDO MODELOS ALTERNATIVOS".center(60, "="))
    
    API_KEY = "minha chave api"
    genai.configure(api_key=API_KEY)
    
    modelos_alternativos = [
        "gemini-1.5-flash",
        "gemini-1.5-pro", 
        "gemini-1.0-pro",
        "gemini-pro",
        "gemini-2.0-flash-exp",
    ]
    
    for modelo in modelos_alternativos:
        print(f"\n🔍 Testando {modelo}...")
        try:
            model = genai.GenerativeModel(modelo)
            response = model.generate_content("Responda com 'OK'")
            print(f"   ✅ {modelo}: FUNCIONA - '{response.text}'")
            
            # Teste rápido de tokens
            tokens = model.count_tokens("Teste").total_tokens
            print(f"   🔢 Tokens: {tokens}")
            
        except Exception as e:
            error_str = str(e)
            if "429" in error_str:
                print(f"   ❌ {modelo}: COTA ESGOTADA")
            else:
                print(f"   ❌ {modelo}: {str(e)[:80]}...")

if __name__ == "__main__":
    # Debug principal
    sucesso = debug_gemini_25_flash()
    
    # Se falhar, verificar alternativas
    if not sucesso:
        verificar_alternativas()
    
    print("\n" + "🚨 LEMBRETE DE SEGURANÇA".center(60, "="))
    print("REVOQUE ESTA CHAVE NO GOOGLE AI STUDIO!")
    print("URL: https://aistudio.google.com/")
    print("=" * 60)