from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.usuario import criar_usuario, buscar_por_email, validar_senha

auth = Blueprint("auth", __name__)

@auth.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip().lower()
        senha = request.form["senha"]

        if not nome or not email or not senha:
            flash("Preencha todos os campos.", "danger")
            return render_template("registro.html")

        if not criar_usuario(nome, email, senha):
            flash("Este e-mail já está cadastrado.", "danger")
            return render_template("registro.html")

        flash("Cadastro realizado! Agora faça login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("registro.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        senha = request.form["senha"]
        usuario = buscar_por_email(email)

        if validar_senha(usuario, senha):
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            return redirect(url_for("dashboard.dashboard_page"))

        flash("E-mail ou senha inválidos.", "danger")

    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
