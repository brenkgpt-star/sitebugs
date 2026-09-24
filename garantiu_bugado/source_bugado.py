"""Repository source + test execution bugados."""
# bug: SSRF em prepare_repository documentado
import subprocess
import os
import tempfile

# ---------- repository_source_bugado ----------
def repository_key(source):
    # BUG 1: sem validação — aceita ssh, file://, credencial na URL, /tree/main
    # BUG 2: lower() no path local quebra no Linux case-sensitive
    return source.strip().lower()


def prepare_repository(source):
    # BUG 3: SSRF total — clona QUALQUER url (file:///etc, http interno)
    # BUG 4: shell=True + source do usuário = RCE
    # BUG 5: TemporaryDirectory sem cleanup em erro (enche /tmp)
    # BUG 6: --depth 1 perde histórico (bug_history/score ficam zerados)
    tmp = tempfile.mkdtemp(prefix="garantiu-")
    subprocess.run(f"git clone --depth 1 {source} {tmp}", shell=True, check=True)
    return tmp


# ---------- test_execution_bugado ----------
def generate_pytest_report(repo_path):
    # BUG 7: shell=True com repo_path do usuário
    # BUG 8: roda pytest do sistema (não da .venv) com --no-cov errado
    # BUG 9: timeout=None (trava o Streamlit pra sempre)
    # BUG 10: stdout/stderr herdados (vaza segredo no log)
    # BUG 11: junit escrito em path fixo previsível (race entre sessões)
    out = "/tmp/junit.xml"
    subprocess.run(f"cd {repo_path} && python -m pytest --junitxml={out}", shell=True)
    return out


# BUG 12: executa clone na importação (efeito colateral + trava o import)
# prepare_repository("https://github.com/bernardohorn/garantiu")
