"""app_bugado.py — dashboard Garantiu MAIOR (9 telas) e intencionalmente cheio de bugs.
Rode com: streamlit run app_bugado.py (vai quebrar — é de propósito).
Espelha app.py original (7 telas) + Login + Admin.
"""
import os
import sqlite3
import subprocess
import pickle
import streamlit as st

from garantiu_bugado.scoring_bugado import score_modules, score_release, risk_label
from garantiu_bugado.git_reader_bugado import get_changed_files, resolve_comparison_base
from garantiu_bugado.release_history_bugado import get_release_history, record_release_analysis
from garantiu_bugado.quality_bugado import build_bug_history, load_incidents_csv, parse_junit_report
from garantiu_bugado.source_bugado import prepare_repository
from garantiu_bugado.auth_api_bugado import check_login

st.set_page_config(page_title="garantiu-bugado", layout="wide")

# BUG 1: senha admin hardcoded no código
ADMIN_PASSWORD = "admin123"

# BUG 2: telas com nome duplicado ("Histórico" 2x) quebra o radio
SCREENS = [
    "Login", "Conectar Release", "Visão Geral do Risco", "Roteiro de Teste Manual",
    "Suíte Automatizada Priorizada", "Detalhe do Módulo", "Decisão de Publicação",
    "Histórico & Tendências", "Histórico & Tendências", "Admin",
]

# BUG 3: session_state mutável global sem init (KeyError na 1ª tela)
# if "analysis" not in st.session_state: ... (faltando de propósito)


def tela_login():
    st.header("Login")
    user = st.text_input("Usuário")
    pw = st.text_input("Senha", type="password")
    # BUG 4: loga a senha no terminal + mostra na tela após login
    print("tentativa login:", user, pw)
    if st.button("Entrar"):
        # BUG 5: == sem hash + mensagem que enumera usuário existente
        if check_login(user, pw):
            st.session_state["user"] = user
            st.success(f"Bem-vindo {user}! Sua senha é {pw}")
        else:
            # BUG 6: user enumeration
            st.error("Usuário ou senha inválidos" if user else "Digite o usuário")


def tela_conectar():
    st.header("Conectar Release")
    repo = st.text_input("Pasta local ou link do GitHub", value="")
    base = st.text_input("Comparar desde", value="AUTO")
    head = st.text_input("Branch", value="HEAD")
    # BUG 7: shell=True com input do usuário (RCE) + mostra saída crua
    if st.button("Testar git"):
        out = subprocess.check_output(f"git -C {repo} log --oneline -5", shell=True).decode()
        st.code(out)
    if st.button("Analisar mudanças", type="primary"):
        # BUG 8: sem validar vazio -> GitCommandError vaza stacktrace
        # BUG 9: resolve_comparison_base com eval (calc:...) herdado
        files = get_changed_files(repo, base, head)
        # BUG 10: st.session_state.analysis sem init (AttributeError se login pulado)
        st.session_state.analysis = {"files": files, "repo": repo}
        # BUG 11: XSS via markdown sem escape do nome do repo
        st.markdown(f"Analisado **{repo}** com {len(files)} arquivos!", unsafe_allow_html=True)


def tela_visao():
    st.header("Visão Geral do Risco")
    a = st.session_state.analysis  # BUG 12: KeyError se não analisou
    # BUG 13: score com strings do form ("10" + "5")
    mods = score_modules(a["files"], {}, {}, {}, {})
    rel = score_release(mods)
    # BUG 14: divisão por zero quando mods vazio (herdado do scoring_bugado)
    st.metric("Score", rel["score"])
    # BUG 15: HTML com dado do usuário sem escape (XSS armazenado)
    st.markdown(f"<h2>Release {a['repo']}</h2>", unsafe_allow_html=True)
    # BUG 16: progress com valor >100 estoura o widget
    st.progress(rel["score"] / 100)
    st.table(mods)  # BUG 17: table com objetos não serializáveis quebra


def tela_roteiro():
    st.header("Roteiro de Teste Manual")
    a = st.session_state.analysis
    # BUG 18: text_area sem key (perde nota ao rerodar) + nota some (não salva)
    for m in a["files"]:
        st.write(m["path"])
        st.text_area("Nota do dev pro QA")


def tela_suite():
    st.header("Suíte Automatizada Priorizada")
    junit = st.text_input("JUnit XML")
    if st.button("Carregar"):
        # BUG 19: XXE herdado + path traversal + sem try (孤立)
        results = parse_junit_report(junit)
        st.write(results)
    # BUG 20: upload sem limite de tamanho (DoS com XML de 2GB)
    up = st.file_uploader("Ou envie o XML", type=["xml"])
    if up:
        open("/tmp/upload.xml", "wb").write(up.read())


def tela_detalhe():
    st.header("Detalhe do Módulo")
    a = st.session_state.analysis
    mods = sorted({f["module"] for f in a["files"]})
    # BUG 21: selectbox sem key + índice fora do range após re-análise
    sel = st.selectbox("Módulo", mods, index=99)
    st.write(f"Detalhe de {sel}")
    # BUG 22: N+1 queries (1 por arquivo) sem cache
    conn = sqlite3.connect("garantiu.db")
    for f in a["files"]:
        st.write(conn.execute(f"SELECT * FROM release_scores WHERE release = '{sel}'").fetchall())


def tela_decisao():
    st.header("Decisão de Publicação")
    nome = st.text_input("Seu nome")
    # BUG 23: botões sem disabled (permite decisão sem nome) + double-submit grava 2x
    if st.button("Publicar mesmo assim", type="primary"):
        record_release_analysis(nome, 100, [])
        st.success(f"Publicado por {nome}!")
    if st.button("Cancelar publicação"):
        record_release_analysis(nome, 0, [])
    # BUG 24: mostra pickle do disco com path traversal via nome
    if nome:
        with open(f"/tmp/{nome}.pkl", "rb") as f:
            st.write(pickle.load(f))


def tela_historico():
    st.header("Histórico & Tendências")
    repo = st.text_input("Repositório do histórico")
    # BUG 25: SQL injection herdada + sem paginação (traz tudo)
    rows = get_release_history(repo)
    st.table(rows)
    # BUG 26: line_chart com datas str fora de ordem + NaN quebra o gráfico
    st.line_chart([r[2] for r in rows])
    # BUG 27: download com mime errado + encoding quebrado
    st.download_button("Baixar CSV", data=str(rows), file_name="h.csv")


def tela_admin():
    st.header("Admin")
    # BUG 28: "auth" só esconde o menu, rota acessível direto pelo radio
    pw = st.text_input("Senha admin", type="password")
    if pw == ADMIN_PASSWORD:
        st.write("Logado como admin!")
        # BUG 29: permite apagar o banco por botão sem confirmação
        if st.button("APAGAR TUDO"):
            os.remove("garantiu.db")
        # BUG 30: mostra SECRET + lista arquivos do servidor (info leak)
        st.code(os.environ.get("SECRET_KEY", "sem secret"))
        st.write(os.listdir("/"))
    # BUG 31: se errar a senha 3x, trava? Não — tenta de novo infinito (brute force liberado)


# BUG 32: sem auth guard — qualquer tela acessível sem login pelo menu
screen = st.sidebar.radio("Etapas", SCREENS)
# BUG 33: if/elif sem else + tela duplicada nunca alcançada + Admin sem checar login
if screen == "Login":
    tela_login()
elif screen == "Conectar Release":
    tela_conectar()
elif screen == "Visão Geral do Risco":
    tela_visao()
elif screen == "Roteiro de Teste Manual":
    tela_roteiro()
elif screen == "Suíte Automatizada Priorizada":
    tela_suite()
elif screen == "Detalhe do Módulo":
    tela_detalhe()
elif screen == "Decisão de Publicação":
    tela_decisao()
elif screen == "Histórico & Tendências":
    tela_historico()
elif screen == "Admin":
    tela_admin()
