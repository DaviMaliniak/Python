from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.tarefa import (
    listar_tarefas, criar_tarefa, buscar_tarefa,
    atualizar_tarefa, excluir_tarefa, concluir_tarefa,
    STATUS_VALIDOS
)
from functools import wraps

tarefas = Blueprint("tarefas", __name__)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper

@tarefas.route("/nova_tarefa", methods=["GET", "POST"])
@login_required
def nova_tarefa():
    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        descricao = request.form["descricao"].strip()
        status = request.form["status"]

        if status not in STATUS_VALIDOS:
            status = "Pendente"

        if not titulo:
            flash("O título é obrigatório.", "danger")
            return render_template("nova_tarefa.html")

        criar_tarefa(titulo, descricao, status, session["usuario_id"])
        flash("Tarefa criada com sucesso!", "success")
        return redirect(url_for("dashboard.dashboard_page"))

    return render_template("nova_tarefa.html")

@tarefas.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    tarefa = buscar_tarefa(id, session["usuario_id"])

    if not tarefa:
        flash("Tarefa não encontrada.", "danger")
        return redirect(url_for("dashboard.dashboard_page"))

    if request.method == "POST":
        atualizar_tarefa(
            id,
            request.form["titulo"].strip(),
            request.form["descricao"].strip(),
            request.form["status"],
            session["usuario_id"]
        )
        flash("Tarefa atualizada!", "success")
        return redirect(url_for("dashboard.dashboard_page"))

    return render_template("editar.html", tarefa=tarefa)

@tarefas.route("/excluir/<int:id>", methods=["POST"])
@login_required
def excluir(id):
    excluir_tarefa(id, session["usuario_id"])
    flash("Tarefa excluída.", "success")
    return redirect(url_for("dashboard.dashboard_page"))

@tarefas.route("/concluir/<int:id>", methods=["POST"])
@login_required
def concluir(id):
    concluir_tarefa(id, session["usuario_id"])
    return redirect(url_for("dashboard.dashboard_page"))
