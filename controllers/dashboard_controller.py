from flask import Blueprint, render_template, request, jsonify, session
from models.tarefa import listar_tarefas, contar_status
import requests

dashboard = Blueprint("dashboard", __name__)

def usuario_logado():
    return "usuario_id" in session

@dashboard.route("/")
def index():
    return render_template("login.html") if not usuario_logado() else render_template(
        "dashboard.html",
        tarefas=listar_tarefas(session["usuario_id"]),
        filtro="Todos",
        counts=contar_status(session["usuario_id"])
    )

@dashboard.route("/dashboard")
def dashboard_page():
    if not usuario_logado():
        from flask import redirect, url_for
        return redirect(url_for("auth.login"))

    status = request.args.get("status", "Todos")
    return render_template(
        "dashboard.html",
        tarefas=listar_tarefas(session["usuario_id"], status),
        filtro=status,
        counts=contar_status(session["usuario_id"])
    )

@dashboard.route("/dashboard/progresso")
def progresso():
    if not usuario_logado():
        from flask import redirect, url_for
        return redirect(url_for("auth.login"))
    return render_template("progresso.html")

@dashboard.route("/api/tarefas")
def api_tarefas():
    if not usuario_logado():
        return jsonify({"erro": "Não autenticado"}), 401

    status = request.args.get("status")
    rows = listar_tarefas(session["usuario_id"], status)
    return jsonify([dict(row) for row in rows])

@dashboard.route("/api/progresso")
def api_progresso():
    if not usuario_logado():
        return jsonify({"erro": "Não autenticado"}), 401
    return jsonify(contar_status(session["usuario_id"]))

@dashboard.route("/api/frase")
def api_frase():
    if not usuario_logado():
        return jsonify({"erro": "Não autenticado"}), 401

    try:
        response = requests.get("https://api.adviceslip.com/advice", timeout=5)
        data = response.json()
        return jsonify({"advice": data["slip"]["advice"]})
    except requests.RequestException:
        return jsonify({"advice": "Continue avançando, uma tarefa de cada vez."})

@dashboard.route("/tema", methods=["POST"])
def tema():
    if not usuario_logado():
        return jsonify({"erro": "Não autenticado"}), 401
    session["modo_escuro"] = request.json.get("dark", False)
    return jsonify({"ok": True})
