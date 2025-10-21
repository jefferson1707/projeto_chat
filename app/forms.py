# Parte 8:  formularios

from flask_wtf import FlaskForm  # Para criar formularios
from wtforms import (
    TextAreaField,
    SubmitField,
    StringField,
    PasswordField,
)  # Campos do formulario, cada campo com sua funcionalidade como descrito.
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    Optional,
    ValidationError
)  # Validadores para os campos do formulario


# Step 1: formulario de login
class LoginForm(FlaskForm):

    # Step 1.1: criar e validar os campos de login
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")


# Step 2: formulario de cadastro de usuario
class RegisterForm(FlaskForm):

    # Step 2.1: criar e validar os campos de cadastro,  com suas condições
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=80)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField(
        "Confirmar Senha", validators=[DataRequired(), EqualTo("senha")]
    )
    submit = SubmitField("Cadastrar")


# Step 3: formulario para enviar mensagem para o Gemini
class MessageForm(FlaskForm):

    # Step 3.1: criar e validar os campos de cadastro,  com suas condições
    content = TextAreaField(
        "Mensagem", validators=[DataRequired(), Length(min=1, max=1000)]
    )
    submit = SubmitField("Enviar")


# Step 4: formulario para criar nova conversa
class ConversationForm(FlaskForm):

    # Step 4.1: criar e validar os campos de cadastro,  com suas condições
    title = StringField(
        "Titulo",
        validators=[DataRequired(), Length(min=1, max=200)],
        render_kw={"placeholder": "Ex: Duvidas sobre Python"},
    )
    submit = SubmitField("Criar Conversa")


# Step 5: formulario para editar perfil
class EditProfileForm(FlaskForm):

    # Step 5.1: criar e validar os campos de cadastro,  com suas condições
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=80)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField(
        "Nova Senha",
        validators=[Optional(), Length(min=6)],
        description="Deixe em branco para manter a senha atual"
    )
    confirmar_senha = PasswordField(
        "Confirmar Nova Senha",
        validators=[EqualTo("senha", message="As senhas devem ser iguais")]
    )
    submit = SubmitField("Atualizar Perfil")

    # Step 5.2: validação customizada apenas se senha foi fornecida
    def validate_senha(self, field):
       
        if field.data and len(field.data) < 6:
            raise ValidationError("A senha deve ter pelo menos 6 caracteres")

    # Step  5.3: só valida confirmação se senha foi fornecida
    def validate_confirmar_senha(self, field):
        
        if self.senha.data and field.data != self.senha.data:
            raise ValidationError("As senhas devem ser iguais")
        
    

# Step 6: formulario para contato/relatar problemas
class ContactForm(FlaskForm):
    
    # Step 6.1: criar e validar os campos de contato
    nome = StringField(
        "Seu Nome", 
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    email = StringField(
        "Seu Email", 
        validators=[DataRequired(), Email()]
    )
    assunto = StringField(
        "Assunto", 
        validators=[DataRequired(), Length(min=5, max=200)]
    )
    mensagem = TextAreaField(
        "Mensagem", 
        validators=[DataRequired(), Length(min=10, max=1000)],
        render_kw={"rows": 6, "placeholder": "Descreva o problema ou dúvida em detalhes..."}
    )
    submit = SubmitField("Enviar Mensagem")