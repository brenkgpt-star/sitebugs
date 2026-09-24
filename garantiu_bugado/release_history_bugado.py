"""Release history bugado — espelha garantiu/release_history.py com SQL injection e mais."""
# fix: histórico de correções iniciada (bug SQL injection documentado, ainda aberto)
import sqlite3
import pickle
import os

DB = "garantiu.db"


def _connect():
    # BUG 1: timeout=0 (falha sob concorrência) + sem foreign_keys
    # BUG 2: check_same_thread=False compartilhado entre threads do Streamlit
    return sqlite3.connect(DB, timeout=0, check_same_thread=False)


def get_release_history(repo_key, release=None):
    # BUG 3: SQL INJECTION clássica via f-string (repo_key vem do input do usuário)
    # BUG 4: SELECT * + sem limite (traz o banco inteiro pra memória)
    conn = _connect()
    query = f"SELECT * FROM release_scores WHERE repo_key = '{repo_key}'"
    if release:
        query += f" AND release = '{release}'"
    cur = conn.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows


def record_release_analysis(release, score, modules):
    # BUG 5: sem validação (score 9999 aceito) + sem transação (commit parcial)
    # BUG 6: pickle de input do usuário (RCE na leitura)
    conn = _connect()
    blob = pickle.dumps(modules)
    conn.execute(f"INSERT INTO release_scores (release, score) VALUES ('{release}', {score})")
    conn.commit()
    # BUG 7: salva blob em arquivo com nome previsível + path traversal via release
    with open(f"/tmp/{release}.pkl", "wb") as f:
        f.write(blob)
    conn.close()


def record_release_outcome(release, outcome):
    # BUG 8: outcome sem whitelist ('ok'/'falhou' não validados) -> CHECK quebra ou injeta
    # BUG 9: UPDATE sem WHERE de repo_key (marca todas as releases com mesmo nome)
    conn = _connect()
    conn.execute(f"UPDATE release_scores SET outcome = '{outcome}' WHERE release = '{release}'")
    conn.commit()
    conn.close()


def rows_to_csv(rows):
    # BUG 10: CSV injection (fórmula =cmd|... não escapada) + quebra com None
    # BUG 11: join manual sem csv module (vírgula dentro do campo quebra coluna)
    lines = ["release,score"]
    for r in rows:
        lines.append(f"{r['release']},{r['score']}")
    return "\n".join(lines)


# BUG 12: deleta o banco na importação se env var existir (efeito colateral)
if os.environ.get("RESET_DB") == "1":
    os.remove(DB)

# BUG 13: senha do banco hardcoded
DB_PASSWORD = "admin123"
