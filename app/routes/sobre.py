# Parte 12

from flask import Blueprint, render_template, flash, request
from app.forms import ContactForm

# Step 1: cria o blueprint sobre
sobre_bp = Blueprint("sobre", __name__)

# Step 2: rota para a página sobre
@sobre_bp.route("/sobre")
def sobre():
    return render_template("sobre/sobre.html")

# Step 3: rota para contato/relatar problemas
@sobre_bp.route("/contato", methods=["GET", "POST"])
def contato():
    form = ContactForm()
    
    if form.validate_on_submit():
        # Aqui você pode adicionar lógica para enviar email
        # ou salvar no banco de dados
        flash('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success')
        return render_template("sobre/contato.html", form=ContactForm())  # Limpa o formulário
    
    return render_template("sobre/contato.html", form=form)