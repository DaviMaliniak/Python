from flask import Flask, session
from models.database import init_db
from controllers.auth_controller import auth
from controllers.tarefa_controller import tarefas
from controllers.dashboard_controller import dashboard

app = Flask(__name__, template_folder="views", static_folder="static")
app.config["SECRET_KEY"] = "troque-esta-chave-em-producao"

app.register_blueprint(auth)
app.register_blueprint(tarefas)
app.register_blueprint(dashboard)

@app.context_processor
def inject_theme():
    return {"modo_escuro": session.get("modo_escuro", False)}

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
