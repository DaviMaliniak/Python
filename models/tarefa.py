from .database import get_db

STATUS_VALIDOS = ["Pendente", "Em andamento", "Concluída"]

def listar_tarefas(usuario_id, status=None):
    conn = get_db()
    if status in STATUS_VALIDOS:
        tarefas = conn.execute(
            "SELECT * FROM tarefas WHERE usuario_id = ? AND status = ? ORDER BY id DESC",
            (usuario_id, status)
        ).fetchall()
    else:
        tarefas = conn.execute(
            "SELECT * FROM tarefas WHERE usuario_id = ? ORDER BY id DESC",
            (usuario_id,)
        ).fetchall()
    conn.close()
    return tarefas

def criar_tarefa(titulo, descricao, status, usuario_id):
    conn = get_db()
    conn.execute(
        "INSERT INTO tarefas (titulo, descricao, status, usuario_id) VALUES (?, ?, ?, ?)",
        (titulo, descricao, status, usuario_id)
    )
    conn.commit()
    conn.close()

def buscar_tarefa(id, usuario_id):
    conn = get_db()
    tarefa = conn.execute(
        "SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?",
        (id, usuario_id)
    ).fetchone()
    conn.close()
    return tarefa

def atualizar_tarefa(id, titulo, descricao, status, usuario_id):
    conn = get_db()
    conn.execute("""
        UPDATE tarefas
        SET titulo = ?, descricao = ?, status = ?
        WHERE id = ? AND usuario_id = ?
    """, (titulo, descricao, status, id, usuario_id))
    conn.commit()
    conn.close()

def excluir_tarefa(id, usuario_id):
    conn = get_db()
    conn.execute(
        "DELETE FROM tarefas WHERE id = ? AND usuario_id = ?",
        (id, usuario_id)
    )
    conn.commit()
    conn.close()

def concluir_tarefa(id, usuario_id):
    conn = get_db()
    conn.execute(
        "UPDATE tarefas SET status = 'Concluída' WHERE id = ? AND usuario_id = ?",
        (id, usuario_id)
    )
    conn.commit()
    conn.close()

def contar_status(usuario_id):
    conn = get_db()
    rows = conn.execute("""
        SELECT status, COUNT(*) AS total
        FROM tarefas WHERE usuario_id = ?
        GROUP BY status
    """, (usuario_id,)).fetchall()
    conn.close()

    counts = {"Pendente": 0, "Em andamento": 0, "Concluída": 0}
    for row in rows:
        counts[row["status"]] = row["total"]
    return counts
