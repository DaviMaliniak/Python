# Painel de Tarefas — MVC

Projeto reorganizado em padrão MVC:

- `models/` → banco e regras dos dados
- `controllers/` → rotas e lógica de controle
- `views/` → páginas HTML
- `static/` → CSS e JavaScript
- `app.py` → inicialização do Flask

## Executar

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Depois acesse `http://127.0.0.1:5000`.

O banco SQLite é criado automaticamente.
