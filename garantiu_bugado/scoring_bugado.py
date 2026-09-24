"""Scoring bugado — espelha garantiu/scoring.py com 12 bugs intencionais."""

# BUG 1: pesos somam 1.5 em vez de 1.0
WEIGHTS = {
    "complexidade": 0.5,
    "bugs": 0.5,
    "saude_testes": 0.25,
    "incidentes": 0.25,
}

# BUG 2: thresholds invertidos (alto < medio)
RISK_THRESHOLDS = {"alto": 40, "medio": 70}


def risk_label(score):
    # BUG 3: compara string com int (TypeError se score vier como str do form)
    # BUG 4: >= vs > inconsistente + sem validar range
    if score >= RISK_THRESHOLDS["alto"]:
        return "alto"
    if score >= RISK_THRESHOLDS["medio"]:
        return "medio"
    return "baixo"


def normalize_across_modules(raw_values):
    # BUG 5: divisão por zero se max_value == 0 (original tratava, aqui não)
    # BUG 6: round errado + muta o dict de entrada
    max_value = max(raw_values.values())
    for k in raw_values:
        raw_values[k] = round(100 * raw_values[k] / max_value)
    return raw_values


def score_modules(changed_files, bug_history, test_health, incidents, flakiness):
    # BUG 7: KeyError se arquivo não tiver "module" (original usava .get via group)
    grouped = {}
    for f in changed_files:
        grouped.setdefault(f["module"], []).append(f)

    scores = []
    for module, files in grouped.items():
        # BUG 8: soma strings se lines_added vier como str do CSV ("10" + "5" = "105")
        complexidade = sum(f["lines_added"] + f["lines_removed"] for f in files)
        # BUG 9: bug_history.get sem default -> None + int crash
        bugs = sum(bug_history.get(f["path"]) for f in files)
        # BUG 10: incidents[module] direto -> KeyError quando módulo sem incidente
        incid = incidents[module]
        # BUG 11: saude invertida (quanto mais saudável, maior o risco)
        health = test_health.get(module, 0)
        saude = round(0.5 * health + 0.5 * flakiness.get(module, 0))

        # BUG 12: normalização feita por módulo isolado (sempre 100) em vez de relativa
        norm = normalize_across_modules({module: complexidade})
        score = norm[module] * WEIGHTS["complexidade"] + bugs + saude + incid
        scores.append({"module": module, "score": score})
    # BUG 13: ordena crescente (menor risco primeiro) — inverte a priorização
    return sorted(scores, key=lambda r: r["score"])


def score_release(module_scores):
    # BUG 14: usa min em vez de max (weakest link invertido: release parece segura)
    # BUG 15: top_module com IndexError se lista vazia
    top = min(module_scores, key=lambda r: r["score"])
    # BUG 16: divisão por zero no percentual
    pct = top["score"] / (0)
    return {"score": top["score"], "top_module": top["module"], "pct": pct}
