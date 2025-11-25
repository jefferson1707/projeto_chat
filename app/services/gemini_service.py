# Parte 11: conexão com a api da gemini

import os
import google.generativeai as genai
from flask import current_app
import json
import time
from typing import List, Dict, Optional
import threading


# Step 1: cria a classe para se comunicar com o Gemini
class GeminiService:

    # Step 1.1 configura a API key do Gemini
    def __init__(self):

        # Step 1.1.1: pega a API key do .env
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY não encontrada no .env")

        # Step 1.1.2: modelo do Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Step 1.1.3: parâmetros padrão de geração
        self.default_generation_config = {
            "temperature": 0.5, # Explicação: quanto mais alto, mais criativo
            "top_p": 0.8, # Explicação:  se concentra nas palavras mais prováveis
            "top_k": 40, # Explicação: limita as palavras mais prováveis
            "max_output_tokens": 850, # Explicação: tamanho máximo da resposta
            "stop_sequences": None, # Explicação: sequência de parada
            "candidate_count": 1,  # Número de respostas alternativas
        }
        
        # Step 1.1.4: configurações de segurança padrão
        self.default_safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH", 
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]

        # Step 1.1.5: Sistema de rate limiting para evitar erro 429
        self._last_request_time = 0
        self._min_request_interval = 2.0  # Mínimo 2 segundos entre requisições
        self._request_lock = threading.Lock()
        self._consecutive_errors = 0
        self._max_consecutive_errors = 5

    # Step 1.1.6: Método interno para controle de rate limiting
    def _apply_rate_limit(self):
        """Aplica rate limiting entre requisições"""
        with self._request_lock:
            current_time = time.time()
            time_since_last = current_time - self._last_request_time
            
            if time_since_last < self._min_request_interval:
                sleep_time = self._min_request_interval - time_since_last
                time.sleep(sleep_time)
            
            self._last_request_time = time.time()

    # Step 1.1.7: Método para tratamento de erro 429 com retry automático
    def _handle_api_call_with_retry(self, api_call_func, *args, **kwargs):
        """
        Executa chamadas à API com retry automático para erro 429
        """
        max_retries = 3
        base_delay = 5  # segundos
        
        for attempt in range(max_retries):
            try:
                # Aplica rate limiting antes de cada tentativa
                self._apply_rate_limit()
                
                # Executa a chamada à API
                result = api_call_func(*args, **kwargs)
                
                # Reseta contador de erros consecutivos em caso de sucesso
                self._consecutive_errors = 0
                return result
                
            except Exception as e:
                error_str = str(e)
                
                # Verifica se é erro 429 (Resource Exhausted)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str.upper():
                    self._consecutive_errors += 1
                    
                    # Se muitos erros consecutivos, aumenta o delay
                    if self._consecutive_errors >= self._max_consecutive_errors:
                        self._min_request_interval = 10.0  # Aumenta intervalo mínimo
                    
                    if attempt < max_retries - 1:
                        # Exponential backoff com jitter
                        wait_time = base_delay * (2 ** attempt) + (0.1 * attempt)
                        current_app.logger.warning(
                            f"⚠️ Erro 429 na tentativa {attempt + 1}/{max_retries}. "
                            f"Aguardando {wait_time:.1f}s..."
                        )
                        time.sleep(wait_time)
                        continue
                    else:
                        current_app.logger.error(f"❌ Falha após {max_retries} tentativas: {error_str}")
                        raise Exception(f"Erro 429: Limite de requisições excedido após {max_retries} tentativas")
                else:
                    # Para outros erros, não faz retry
                    current_app.logger.error(f"❌ Erro não recuperável: {error_str}")
                    raise e
        
        raise Exception("Falha inesperada no retry mechanism")

    # Step 1.2: cria o método para enviar mensagem
    def send_message(self, message, conversation_history=None, 
                   generation_config=None, safety_settings=None,
                   stream=False):
        
        # Step 1.2.1: combina configurações padrão com personalizadas
        final_config = self.default_generation_config.copy()
        if generation_config:
            final_config.update(generation_config)

        final_safety = self.default_safety_settings.copy()
        if safety_settings:
            final_safety = safety_settings

        # Step 1.2.3: envia mensagem para o Gemini e retorna resposta
        try:
            generation_config_obj = genai.types.GenerationConfig(**final_config)
            
            # Define a função de chamada à API
            def api_call():
                if conversation_history:
                    # Step 1.2.3.1: se a conversa tem histórico, usa contexto da conversa
                    chat = self.model.start_chat(history=conversation_history)
                    if stream:
                        # Explicação: modo streaming para resposta em tempo real
                        response = chat.send_message(
                            message, 
                            generation_config=generation_config_obj,
                            safety_settings=final_safety,
                            stream=True
                        )
                        return response, True
                    else:
                        response = chat.send_message(
                            message, 
                            generation_config=generation_config_obj,
                            safety_settings=final_safety
                        )
                else:
                    # Step 1.2.3.2: no caso de nova conversa
                    if stream:
                        response = self.model.generate_content(
                            message, 
                            generation_config=generation_config_obj,
                            safety_settings=final_safety,
                            stream=True
                        )
                        return response, True
                    else:
                        response = self.model.generate_content(
                            message, 
                            generation_config=generation_config_obj,
                            safety_settings=final_safety
                        )
                
                return response.text, True

            # Executa com tratamento de erro 429
            result, success = self._handle_api_call_with_retry(api_call)
            return result, success

        except Exception as e:
            error_msg = f"Erro ao comunicar com Gemini: {str(e)}"
            current_app.logger.error(error_msg)
            return error_msg, False

    # Step 1.3: método para gerar múltiplas versões da resposta
    def generate_multiple_candidates(self, message, num_candidates=3, 
                                   conversation_history=None):
        # Step 1.3.1: gera várias versões diferentes da mesma resposta
        try:
            config = self.default_generation_config.copy()
            config["candidate_count"] = num_candidates
            config["temperature"] = 0.8  # Explicação: aumenta criatividade para variedade
            
            generation_config_obj = genai.types.GenerationConfig(**config)
            
            def api_call():
                if conversation_history:
                    chat = self.model.start_chat(history=conversation_history)
                    response = chat.send_message(
                        message,
                        generation_config=generation_config_obj,
                        safety_settings=self.default_safety_settings
                    )
                else:
                    response = self.model.generate_content(
                        message,
                        generation_config=generation_config_obj,
                        safety_settings=self.default_safety_settings
                    )
                
                # Step 1.3.2: retorna todas as candidatas geradas
                candidates = [candidate.text for candidate in response.candidates]
                return candidates, True
            
            # Executa com tratamento de erro 429
            return self._handle_api_call_with_retry(api_call)
            
        except Exception as e:
            error_msg = f"Erro ao gerar múltiplas candidatas: {str(e)}"
            current_app.logger.error(error_msg)
            return [error_msg], False

    # Step 1.4: método para contar tokens
    def count_tokens(self, text, conversation_history=None):
        try:
            def api_call():
                if conversation_history:
                    chat = self.model.start_chat(history=conversation_history)
                    count_data = chat.count_tokens(text)
                else:
                    count_data = self.model.count_tokens(text)
                    
                return count_data.total_tokens, True
            
            # Executa com tratamento de erro 429
            return self._handle_api_call_with_retry(api_call)
            
        except Exception as e:
            error_msg = f"Erro ao contar tokens: {str(e)}"
            current_app.logger.error(error_msg)
            return error_msg, False

    # Step 1.5: método para análise de conteúdo
    def analyze_content(self, text):
        # Step 1.5.1: analisa o conteúdo do texto para segurança
        try:
            def api_call():
                response = self.model.generate_content(
                    f"Analise este conteúdo para segurança e appropriateness: {text}"
                )
                
                token_count = self.model.count_tokens(text).total_tokens
                
                analysis_result = {
                    "text_length": len(text),
                    "token_count": token_count,
                    "safety_analysis": response.text,
                    "is_likely_safe": True  # Explicação: poderia implementar lógica mais sofisticada
                }
                
                return analysis_result, True
            
            # Executa com tratamento de erro 429
            return self._handle_api_call_with_retry(api_call)
            
        except Exception as e:
            error_msg = f"Erro ao analisar conteúdo: {str(e)}"
            current_app.logger.error(error_msg)
            return {"error": error_msg}, False

    # Step 1.13: Método para verificar status do serviço
    def check_service_status(self):
        """Verifica se o serviço está respondendo normalmente"""
        try:
            # Teste simples com contagem de tokens
            test_text = "Teste de conexão"
            tokens, success = self.count_tokens(test_text)
            
            status_info = {
                "status": "online" if success else "offline",
                "consecutive_errors": self._consecutive_errors,
                "min_request_interval": self._min_request_interval,
                "last_request_time": self._last_request_time
            }
            
            return status_info, success
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "consecutive_errors": self._consecutive_errors
            }, False

    # Step 1.14: Método para ajustar rate limiting dinamicamente
    def adjust_rate_limits(self, requests_per_minute=30):
        """Ajusta os limites de rate limiting dinamicamente"""
        if requests_per_minute <= 0:
            raise ValueError("requests_per_minute deve ser maior que 0")
        
        self._min_request_interval = 60.0 / requests_per_minute
        current_app.logger.info(f"✅ Rate limiting ajustado para {requests_per_minute} req/min")
        
        return {
            "requests_per_minute": requests_per_minute,
            "min_interval_seconds": self._min_request_interval
        }

    # Step 1.15: Método para resetar contadores de erro
    def reset_error_counters(self):
        """Reseta os contadores de erro consecutivos"""
        self._consecutive_errors = 0
        self._min_request_interval = 2.0  # Volta ao valor padrão
        current_app.logger.info("✅ Contadores de erro resetados")
        return True

    # Step 1.6: método para configurações de segurança personalizadas
    def set_safety_level(self, level="medium"):
        # Step 1.6.1: define o nível de segurança de forma simplificada
        safety_levels = {
            "block_none": "BLOCK_NONE",
            "block_only_high": "BLOCK_ONLY_HIGH", 
            "block_medium_and_above": "BLOCK_MEDIUM_AND_ABOVE",
            "block_low_and_above": "BLOCK_LOW_AND_ABOVE"
        }
        
        threshold = safety_levels.get(level, "BLOCK_MEDIUM_AND_ABOVE")
        
        for setting in self.default_safety_settings:
            setting["threshold"] = threshold
            
        return self.default_safety_settings

    # Step 1.7: método para salvar e carregar configurações
    def save_config_to_file(self, filename="gemini_config.json"):
        """Salva a configuração atual em um arquivo"""
        try:
            config_data = {
                "generation_config": self.default_generation_config,
                "safety_settings": self.default_safety_settings
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
                
            return True, f"Configuração salva em {filename}"
        except Exception as e:
            return False, f"Erro ao salvar configuração: {str(e)}"

    # Step 1.8: método para carregar configurações de um arquivo
    def load_config_from_file(self, filename="gemini_config.json"):
        # Step 1.8.1: carrega configuração de um arquivo
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                
            self.default_generation_config.update(config_data.get("generation_config", {}))
            self.default_safety_settings = config_data.get("safety_settings", self.default_safety_settings)
            
            return True, "Configuração carregada com sucesso"
        except Exception as e:
            return False, f"Erro ao carregar configuração: {str(e)}"

    # Step 1.9: método para listar modelos disponíveis
    @staticmethod
    def list_available_models():
        # Step 1.9.1: lista todos os modelos disponíveis na API
        try:
            models = genai.list_models()
            model_list = []
            
            for model in models:
                model_info = {
                    "name": model.name,
                    "display_name": model.display_name,
                    "description": model.description,
                    "input_token_limit": model.input_token_limit,
                    "output_token_limit": model.output_token_limit,
                    "supported_generation_methods": model.supported_generation_methods
                }
                model_list.append(model_info)
                
            return model_list, True
        except Exception as e:
            error_msg = f"Erro ao listar modelos: {str(e)}"
            return [error_msg], False

    # Step 1.10: método para atualizar parâmetros padrão
    def update_default_config(self, **new_params):
        # Step 1.10.1: atualiza os parâmetros padrão de geração
        self.default_generation_config.update(new_params)
        return self.default_generation_config

    # Step 1.11: método para obter configuração atual
    def get_current_config(self):
        # Step 1.11.1: retorna a configuração atual
        return {
            "generation_config": self.default_generation_config.copy(),
            "safety_settings": self.default_safety_settings.copy(),
            "rate_limiting": {
                "min_request_interval": self._min_request_interval,
                "consecutive_errors": self._consecutive_errors,
                "max_consecutive_errors": self._max_consecutive_errors
            }
        }

    # Step 1.12: método para resetar configurações
    def reset_to_defaults(self):
        # Step 1.12.1: reseta todas as configurações para os valores padrão
        self.default_generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048,
            "stop_sequences": None,
            "candidate_count": 1,
        }
        # Também reseta o rate limiting
        self.reset_error_counters()
        return self.get_current_config()


# Step 2: cria a instância global do serviço
gemini_service = GeminiService()