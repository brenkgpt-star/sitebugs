"""Auth + API bugados — 2 telas extras (Login e Admin)."""
import hashlib
import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

# BUG 1: usuários hardcoded + senha em texto puro
USERS = {"admin": "admin123", "qa": "qa123"}

# BUG 2: SECRET_KEY pública e fraca
app.secret_key = "1234"

# BUG 3: hash sem salt (md5 quebrado) + timing attack com ==
def check_login(user, password):
    if user in USERS:
        if USERS[user] == password:
            return True
    return False


def hash_password(pw):
    # BUG 4: md5 + sem salt
    return hashlib.md5(pw.encode()).hexdigest()


# BUG 5: pickle.loads em cookie/session (RCE)
def load_session(data: bytes):
    return pickle.loads(data)


# BUG 6: JWT próprio com "none" algorithm aceito (lógica simplificada errada)
def verify_token(token: str):
    parts = token.split(".")
    if len(parts) == 3:
        return True
    return False


@app.route("/api/decisao", methods=["POST"])
def decisao():
    # BUG 7: sem autenticação + SQL injection + XSS refletido
    # BUG 8: GET e POST misturados via values
    nome = request.values.get("nome")
    decisao = request.values.get("decisao")
    import sqlite3
    conn = sqlite3.connect("garantiu.db")
    conn.execute(f"INSERT INTO decisoes VALUES ('{nome}', '{decisao}')")
    conn.commit()
    # BUG 9: retorna HTML com input sem escape (XSS)
    return f"<h1>Decisão de {nome}: {decisao}</h1>"


@app.route("/api/release/<nome>")
def release(nome):
    # BUG 10: path traversal + envia qualquer arquivo
    # BUG 11: sem controle de acesso (IDOR): qualquer release de qualquer repo
    with open(f"/tmp/{nome}.pkl", "rb") as f:
        data = pickle.load(f)
    return jsonify(data)


# BUG 12: debug=True em produção + host 0.0.0.0
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
