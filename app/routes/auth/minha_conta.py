# Parte 9: parte responsavel pela conta do usuario

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user, logout_user
from app.forms import ConversationForm,  EditProfileForm
from app.models import User, Conversation, Message
from app import db
from app.services.gemini_service import gemini_service 
from datetime import datetime


# Step 1: cria o blueprint auth
minha_conta_bp = Blueprint("minha_conta", __name__)


# Step 2: rota para login
@minha_conta_bp.route("/minha-conta")
@login_required  # Explicação: Obrigatorio estar logado
def minha_conta():

    # Step 2.1: pagina principal do usuario
    conversas = (
        Conversation.query.filter_by(user_id=current_user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )

    return render_template("minha_conta/minha_conta.html", conversas=conversas)


# Step 3: rota para editar dados do usuario
@minha_conta_bp.route("/editar-perfil", methods=["GET", "POST"])
@login_required
def editar_perfil():

    # Step 3.1: Preenche form com dados atuais
    form = EditProfileForm(obj=current_user)

    # Step 3.2: atualiza apenas os campos permitidos
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.senha.data:
            # explicassao do password_hash: senha criptografada
            current_user.password_hash = form.senha.data

        db.session.commit()
        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for("minha_conta.minha_conta"))

    return render_template("minha_conta/editar_perfil.html", form=form)


# Step 4: rota para historico de conversas
@minha_conta_bp.route("/historico-conversas")
@login_required
def historico_conversas():

    # Step 4.1:  historico completo de todas as conversas
    conversas = (
        Conversation.query.filter_by(user_id=current_user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )

    return render_template("minha_conta/historico_conversas.html", conversas=conversas)


# Step 5: rota para apagar uma conversa
@minha_conta_bp.route("/apagar-conversa/<int:conversa_id>", methods=["POST"])
@login_required
def apagar_conversa(conversa_id):
    # Step 5.1:  apagar uma conversa específica
    conversa = Conversation.query.filter_by(
        id=conversa_id, user_id=current_user.id
    ).first_or_404()  # explicação: # first_or_404() → se não encontrar, retorna erro 404

    # Step 5.2: apaga a conversa (e todas as mensagens por cascade)
    db.session.delete(conversa)
    db.session.commit()

    flash("Conversa apagada com sucesso!", "success")
    return redirect(url_for("minha_conta.historico_conversas"))


# Step 6: rota para apagar todas as conversas
@minha_conta_bp.route("/apagar-todas-conversas", methods=["GET", "POST"])
@login_required
def apagar_todas_conversas():

     # Step 6.1: mostra página de confirmação
    if request.method == "GET":
        return render_template("minha_conta/apagar_todas_conversas.html")
    
    # Step 6.2: se POST, processa a exclusão
    if request.method == "POST":
        if request.form.get("confirmacao") == "APAGAR_TODAS":
            conversas = Conversation.query.filter_by(user_id=current_user.id).all()
            
            total_conversas = len(conversas)

            for conversa in conversas:
                db.session.delete(conversa)
            
            db.session.commit()
            flash("Todas as conversas foram apagadas!", "success")
            return redirect(url_for("minha_conta.minha_conta"))
        else:
            flash("Confirmação incorreta. Nenhuma conversa foi apagada.", "error")
            return redirect(url_for("minha_conta.apagar_todas_conversas"))

# Step 7: rota para apagar conta
@minha_conta_bp.route("/apagar-conta", methods=["GET", "POST"])
@login_required
def apagar_conta():

    # Step 7.1: apagar permanentemente a conta do usuário
    if request.method == "POST":

        if (
            request.form.get("confirmacao") == "APAGAR_CONTA"
        ):  # Explicação: escolhi APAGAR_CONTA porque, difícil digitar por acidente e deixa explícito o que está fazendo.

            # Step 7.1.1: primeiro apaga todas as conversas do usuário
            conversas = Conversation.query.filter_by(user_id=current_user.id).all()
            for conversa in conversas:
                db.session.delete(conversa)

            #  Step 7.1.2: depois apaga o usuário
            user_para_apagar = User.query.get(current_user.id)
            db.session.delete(user_para_apagar)
            db.session.commit()

            # Step 7.1.3: desloga o usuário
            logout_user()
            flash("Sua conta foi apagada permanentemente.", "info")
            return redirect(url_for("home.index"))

        else:
            flash("Confirmação incorreta. Conta não apagada.", "error")

    return render_template("minha_conta/apagar_conta.html")


# Step 8: rota para criar nova conversa
@minha_conta_bp.route("/nova-conversa", methods=["GET", "POST"])
@login_required
def nova_conversa():

    # Step 8.1: cria uma nova conversa com o Gemini
    form = ConversationForm()

    # Step 8.2: cria um novo objeto Conversation com os dados do formulário
    if form.validate_on_submit():
        nova_conversa = Conversation(title=form.title.data, user_id=current_user.id)
        db.session.add(nova_conversa)
        db.session.commit()

        flash("Nova conversa criada com sucesso!", "success")
        return redirect(
            url_for("minha_conta.ver_conversa", conversa_id=nova_conversa.id)
        )

    return render_template("minha_conta/nova_conversa.html", form=form)


# Step 9: rota para ver uma conversa
@minha_conta_bp.route("/conversa/<int:conversa_id>")
@login_required
def ver_conversa(conversa_id):

    # Step 9.1: visualiza uma conversa específica
    conversa = Conversation.query.filter_by(
        id=conversa_id, user_id=current_user.id
    ).first_or_404()
    mensagens = (
        Message.query.filter_by(conversation_id=conversa_id)
        .order_by(Message.timestamp.asc())
        .all()
    )  # Explicação: busca todas as mensagens desta conversa, ordenadas por data

    return render_template("minha_conta/ver_conversa.html", conversa=conversa, mensagens=mensagens)

# Step 10: rota para enviar mensagem
@minha_conta_bp.route('/conversa/<int:conversa_id>/enviar-mensagem', methods=['POST'])
@login_required
def enviar_mensagem(conversa_id):

    # Step 10.1: Envia mensagem para o Gemini e salva no banco
    conversa = Conversation.query.filter_by(id=conversa_id, user_id=current_user.id).first_or_404()
    
    # Step 10.2: verifica se a mensagem foi enviada
    content = request.form.get('content')
    if not content:
        flash('Mensagem não pode estar vazia.', 'error')
        return redirect(url_for('minha_conta.ver_conversa', conversa_id=conversa_id))
    
    # Step 10.3: salva mensagem do usuário
    mensagem_usuario = Message(
        content=content,
        role='user',
        conversation_id=conversa_id
    )
    db.session.add(mensagem_usuario)
    db.session.flush()  #  Explicação: garante que o ID é gerado
    
    # Step 10.4: busca histórico da conversa para contexto
    historico_mensagens = Message.query.filter_by(conversation_id=conversa_id).order_by(Message.timestamp.asc()).all()
    
    # Step 10.5: prepara histórico para o Gemini
    historico_gemini = []
    for msg in historico_mensagens:
        historico_gemini.append({
            'role': 'user' if msg.role == 'user' else 'model', # Explicação: role usado para identificar "quem disse o que na conversa"
            'parts': [msg.content]
        })
    
    # Step 10.6: envia para o Gemini
    resposta_texto, sucesso = gemini_service.send_message(content, historico_gemini)
    
    # Step 10.7: salva resposta do Gemini
    mensagem_gemini = Message(
        content=resposta_texto,
        role='assistant', 
        conversation_id=conversa_id
    )
    db.session.add(mensagem_gemini)
    
    # Step 10.8: atualiza timestamp da conversa
    conversa.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    if sucesso:
        flash('Resposta recebida do Gemini!', 'success')
    else:
        flash('Erro ao obter resposta do Gemini.', 'error')
    
    return redirect(url_for('minha_conta.ver_conversa', conversa_id=conversa_id))