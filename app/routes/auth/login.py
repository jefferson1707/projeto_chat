# Parte 5

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.forms import LoginForm, RegisterForm
from app.models import User
from app import db, bcrypt

# Step 1: cria o blueprint auth
auth_bp = Blueprint("auth", __name__)


# Step 2: rota para login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # Step 2.1: se usuário já está logado, redireciona para minha conta
    if current_user.is_authenticated:
        return redirect(url_for('minha_conta.minha_conta'))
    
    # Step 2.2: cria o formulário de login
    form = LoginForm()

    # Step 2.3: se o formulário for valido, loga o usuário e redireciona para minha conta
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.senha.data):
            login_user(user)
            flash('Logado com sucesso', 'success')
            return redirect(url_for('minha_conta.minha_conta'))
        
        else:
            flash('Email ou senha incorretos', 'error')

    return render_template("auth/login.html", form=form)


# Step 3: rota para registro
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    
    # Step 3.1: redireciona para minha conta se usuário estiver logado
    if current_user.is_authenticated:
        return redirect(url_for('minha_conta.minha_conta'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Step 3.2: verifica se email ou username já existem
        existing_user = User.query.filter(
            (User.email == form.email.data) | (User.username == form.username.data)
        ).first()
        
        if existing_user:
            flash('Email ou nome de usuário já cadastrado.', 'error')
            return render_template('auth/register.html', form=form)
        
        # Step 3.3: cria novo usuário (senha ainda não criptografada)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=form.senha.data
        )
        
        # Step 3.4: criptografa a senha
        new_user.set_password(form.senha.data)

        db.session.add(new_user)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
def logout():
    """Faz logout do usuário"""
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('home.index'))

               
               