# Parte 7: este arquivo usa class para definir a estrutura do banco de dados
# sem a necessidade de passar comandos brutos de SQL

from datetime import datetime

# para os métodos que o sistema de login espera
# nos dá 4 métodos essenciais de graça, sem precisar implementar manualmente.
from flask_login import (
    UserMixin,
)  # é uma classe do Flask-Login que fornece implementações padrão,

from app import db, login_manager, bcrypt

# Step 1: função necessária para o Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Step 2:  Herda de UserMixin (login) e db.Model (banco de dados)
class User(UserMixin, db.Model):

    #  Step 2.1: passar o nome da tabela no banco
    __tablename__ = "users"

    # Step 2.2: # ID coluna
    id = db.Column(db.Integer, primary_key=True)

    # Step 2.3: # Nome coluna
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Step 2.4: # Email coluna
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Step 2.5: # Senha coluna
    password_hash = db.Column(db.String(130), nullable=False)

    # Step 2.6: # Data de criacao coluna
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Step 2.7: Relacionamento com as conversas do usuário
    conversations = db.relationship('Conversation', 
                                  backref='user', 
                                  lazy='dynamic',
                                  cascade='all, delete-orphan'
    )

    # Step 2.7: Metodos para criptografia
    def set_password(self, password):
        # Explicação: criptografa a senha e armazena o hash
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Step 2.8: Metodos para criptografia
    def check_password(self, password):
        # Explicação: Verifica se a senha está correta
        return bcrypt.check_password_hash(self.password_hash, password)
    

    # Step 2.9: método para representação em texto (debug)
    def __repr__(self):
        return f"<User {self.username}>"


# Step 3: Herda de db.Model
class Conversation(db.Model):

    # Step 3.1: passar o nome da tabela no banco
    __tablename__ = "conversations"

    # Step 3.2: ID coluna
    id = db.Column(db.Integer, primary_key=True)

    # Step 3.3: título da conversa
    title = db.Column(db.String(200), nullable=False, default="Nova Conversa")

    # Step 3.4: data e hora quando a conversa foi criada
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Step 3.5: data e hora quando a conversa foi atualizada
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Step 3.6: chave estrangeira para o usuário dono da conversa
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Step 3.7: relacionamento com as mensagens da conversa
    messages = db.relationship('Message', 
                              backref='conversation', 
                              lazy='dynamic',
                              cascade='all, delete-orphan'
    )

    # Step 3.8: Metodos para representação em texto (debug)
    def __repr__(self):
        return f"<Conversation {self.title}>"


# Step 4:  Herda de db.Model
class Message(db.Model):

    # Step 4.1: passar o nome da tabela no banco
    __tablename__ = "messages"

    # Step 4.2: ID coluna
    id = db.Column(db.Integer, primary_key=True)

    # Step 4.3: Conteúdo da mensagem - texto longo
    content = db.Column(db.Text, nullable=False)

    # Step 4.4: Data e hora quando a mensagem foi enviada
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Step 4.5: 'user' ou 'assistant' - quem enviou a mensagem
    role = db.Column(db.String(20), nullable=False)

    # Step 4.6: chave estrangeira para a conversa
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False)

    # Step 4.7: Metodos para representação em texto (debug)
    def __repr__(self):
        return f"<Message {self.id} ({self.role})>"
