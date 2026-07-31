from werkzeug.security import generate_password_hash, check_password_hash
from .database import get_db

def criar_usuario(nome, email, senha):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, generate_password_hash(senha))
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def buscar_por_email(email):
    conn = get_db()
    usuario = conn.execute(
        "SELECT * FROM usuarios WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return usuario

def validar_senha(usuario, senha):
    return usuario and check_password_hash(usuario["senha"], senha)
