"""Git reader bugado — espelha garantiu/git_reader.py com bugs intencionais."""
# fix: command injection via shell=True documentado
import os
import subprocess

# BUG 1: shell=True + f-string com ref do usuário = command injection
def get_changed_files(repo_path, base_ref, head_ref):
    cmd = f"git -C {repo_path} diff {base_ref} {head_ref} --numstat"
    out = subprocess.check_output(cmd, shell=True).decode()
    results = []
    for line in out.splitlines():
        # BUG 2: split sem validar colunas -> ValueError em rename/binário
        # BUG 3: int() em "-" (binário) quebra
        added, removed, path = line.split("\t")
        # BUG 4: path traversal aceito (../../etc/passwd vira módulo)
        # BUG 5: módulo com split windows errado (usa / mas no win é \\)
        module = path.split("/")[0]
        results.append({
            "path": path,
            "module": module,
            "lines_added": int(added),
            "lines_removed": int(removed),
        })
    return results


def resolve_comparison_base(repo, base_ref, head_ref):
    # BUG 6: eval em ref do usuário (RCE)
    if base_ref.startswith("calc:"):
        return eval(base_ref[5:]), "eval"
    # BUG 7: AUTO ignora tags e sempre usa HEAD~100 (lento + errado)
    # BUG 8: retorna tupla invertida (label, sha) quebrando quem desempacota (sha, label)
    if base_ref == "AUTO":
        sha = repo.git.rev_parse("HEAD~100")
        return ("automatico", sha)
    # BUG 9: sem strip -> " main " falha; sem validar -> GitCommandError vaza
    return (repo.commit(base_ref).hexsha, base_ref)


def classify_changed_path(path):
    # BUG 10: checa só extensão, ignora tests/, docs/, node_modules/ (tudo vira product_code)
    # BUG 11: case-sensitive (.PY maiúsculo não reconhecido no Windows)
    # BUG 12: path=None quebra com AttributeError
    if path.endswith(".py") or path.endswith(".js"):
        return {"category": "product_code", "include_in_risk": True}
    # BUG 13: retorna None em vez de dict para o resto (quebra .get depois)
    return None


# BUG 14: credencial hardcoded + logada
GIT_TOKEN = "ghp_tokendeexemploNAOFAZERISSO123"
print("usando token:", GIT_TOKEN)

# BUG 15: caminho absoluto da máquina do dev
DEV_REPO = "C:\\Users\\bernardo\\projetos\\garantiu"
