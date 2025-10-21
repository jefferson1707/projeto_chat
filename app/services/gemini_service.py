# Parte 11: conexão com a api da gemini

import os
import google.generativeai as genai
from flask import current_app
import json
from typing import List, Dict, Optional


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
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
        
        # Step 1.1.3: parâmetros padrão de geração
        self.default_generation_config = {
            "temperature": 0.7, # Explicação: quanto mais alto, mais criativo
            "top_p": 0.8, # Explicação:  se concentra nas palavras mais prováveis
            "top_k": 40, # Explicação: limita as palavras mais prováveis
            "max_output_tokens": 2048, # Explicação: tamanho máximo da resposta
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
            
            if conversation_history:
                # Step 1.2.3.1: se a conversa tem histórico, usa contexto da conversa
                chat = self.model.start_chat(history=conversation_history)
                if stream:
                    #  Explicação: modo streaming para resposta em tempo real
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

        except Exception as e:
            error_msg = f"Erro ao comunicar com Gemini: {str(e)}"
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
            
        except Exception as e:
            error_msg = f"Erro ao gerar múltiplas candidatas: {str(e)}"
            return [error_msg], False

    # Step 1.4: método para contar tokens
    def count_tokens(self, text, conversation_history=None):
       
        try:
            if conversation_history:
                chat = self.model.start_chat(history=conversation_history)
                count_data = chat.count_tokens(text)
            else:
                count_data = self.model.count_tokens(text)
                
            return count_data.total_tokens, True
        except Exception as e:
            error_msg = f"Erro ao contar tokens: {str(e)}"
            return error_msg, False

    # Step 1.5: método para análise de conteúdo
    def analyze_content(self, text):
        # Step 1.5.1: analisa o conteúdo do texto para segurança
        try:
           
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
            
        except Exception as e:
            error_msg = f"Erro ao analisar conteúdo: {str(e)}"
            return {"error": error_msg}, False

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
            "safety_settings": self.default_safety_settings.copy()
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
        return self.get_current_config()


# Step 2: cria a instância global do serviço
gemini_service = GeminiService()