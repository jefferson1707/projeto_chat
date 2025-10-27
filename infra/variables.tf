variable "render_api_key" {
  description = "API key da conta Render"
  type        = string
  sensitive   = true
}

variable "render_owner_id" {
  description = "Owner ID da conta Render (User ID ou Team ID)"
  type        = string
}

variable "gemini_api_key" {
  description = "Chave da API Gemini usada no app Flask"
  type        = string
  sensitive   = true
}

variable "flask_secret_key" {
  description = "Chave secreta para o Flask"
  type        = string
  sensitive   = true
}