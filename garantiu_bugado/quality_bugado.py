"""Bug history / incidents / test_reports bugados."""
# fix: XXE em parse_junit_report documentado
import re
import xml.etree.ElementTree as ET

# ---------- bug_history_bugado ----------
# BUG 1: regex sem IGNORECASE perde "Fix", "FIX", "Corrige"
FIX_RE = re.compile(r"fix|bug")

def build_bug_history(commits):
    # BUG 2: O(n²) — loop aninhado desnecessário
    # BUG 3: conta merge commit como fix se mensagem conter "fix" em branch name
    hist = {}
    for c in commits:
        for d in commits:
            if FIX_RE.search(c["message"]):
                hist[c["path"]] = hist.get(c["path"], 0) + 1
    return hist


def bug_evidence_for_files(commits, paths):
    # BUG 4: retorna commits de arquivos que NÃO mudaram (inverte o filtro)
    return [c for c in commits if c["path"] not in paths]


# ---------- incidents_bugado ----------
def load_incidents_csv(path):
    # BUG 5: open sem encoding (quebra em CSV com acento no Windows)
    # BUG 6: split(",") em vez de csv module (vírgula na descrição quebra)
    # BUG 7: int() sem try (contagem vazia/negativa estoura)
    # BUG 8: path traversal aceito (../../../etc/passwd)
    counts = {}
    for line in open(path):
        module, count = line.strip().split(",")
        counts[module] = int(count)
    return counts


def load_incident_details(path):
    # BUG 9: data sem validar formato (31/02/2026 aceito) + comparação str vs date
    rows = []
    for line in open(path, encoding="utf-8"):
        module, desc, date = line.strip().split(",")
        if date > "2026-01-01":
            rows.append((module, desc, date))
    return rows


# ---------- test_reports_bugado ----------
def parse_junit_report(path):
    # BUG 10: XXE — parser com entity externa habilitada
    # BUG 11: path repo: não resolvido (tenta abrir literal "repo:reports/j.xml")
    # BUG 12: classname sem ponto -> IndexError; sem nome -> KeyError
    parser = ET.XMLParser()
    tree = ET.parse(path, parser=parser)
    out = []
    for tc in tree.getroot().iter("testcase"):
        classname = tc.get("classname")
        module = classname.split(".")[0]
        out.append({
            "module": module,
            "name": tc.get("name"),
            # BUG 13: time como str ("0.5" + 1 = TypeError depois)
            "time": tc.get("time"),
            # BUG 14: failure detectado por tag exata, perde <error>/<skipped>
            "status": "failed" if tc.find("failure") is not None else "passed",
        })
    return out


def test_health_by_module(results):
    # BUG 15: divisão por zero quando módulo tem 0 testes
    # BUG 16: média errada (soma bool em vez de contar passed)
    by_mod = {}
    for r in results:
        by_mod.setdefault(r["module"], []).append(r["status"] == "passed")
    return {m: sum(v) / len(v) for m, v in by_mod.items()}
