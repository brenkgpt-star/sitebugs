# Análise do repo bernardohorn/garantiu + Bugs captados

> Repo analisado: https://github.com/bernardohorn/garantiu (50 commits, Python + Streamlit)
> Estrutura real: `app.py` (937 linhas, 7 telas), `garantiu/` (15 módulos), `tests/` (17 arquivos), `sample_data/`, `requirements.txt`
> Telas reais: Conectar Release, Visão Geral do Risco, Roteiro de Teste Manual, Suíte Automatizada Priorizada, Detalhe do Módulo, Decisão de Publicação, Histórico & Tendências
> Cálculo real: score 0-100, 4 fatores com peso 25% cada (complexidade, bugs, saude_testes, incidentes), normalização relativa ao módulo máximo, score da release = maior score de módulo.

## Bugs / fragilidades REAIS captados no código original

Estes são pontos reais observados lendo `app.py`, `git_reader.py`, `repository_source.py`, `test_execution.py`, `release_history.py`, `scoring.py`:

1. **`app.py:387-392` — `raise ValueError` dentro de `with st.spinner` sem try local**: se o usuário informar arquivo `modelo-*`, a exceção sobe para o handler genérico da linha 930 e derruba a tela inteira em vez de mostrar erro no campo.
2. **`_discover_repository_quality_sources` — clone temporário a cada tecla**: `prepare_repository()` faz `git clone --bare` com timeout de 120s toda vez que `repo_input`/`head_ref` muda. Digitar a URL dispara vários clones sequenciais, lento e com condição de corrida no cache de sessão.
3. **`repository_source.py` — SSRF parcial**: valida `github.com` + regex de owner/name, mas aceita qualquer repo público e clona com credencial da máquina (`credential helper`). Um link malicioso para repo gigante estoura os 120s / disco temporário.
4. **`test_execution.py` — RCE local por design**: `generate_pytest_report()` executa `python -m pytest` da pasta analisada com as permissões do Streamlit. Analisar repo de terceiro com `conftest.py` malicioso executa código arbitrário. O aviso existe mas o checkbox vem marcado por preferência de sessão.
5. **`test_execution.py:23-25` — `untracked_files` com `is_relative_to`**: qualquer arquivo novo fora de `garantiu-junit/` marca `working_tree_dirty=True`, mesmo que irrelevante (ex.: `.venv`, `node_modules`), gerando falso alerta "testes com alterações locais".
6. **`scoring.py` — normalização relativa enganosa**: `normalize_across_modules` divide pelo máximo. Se só 1 módulo mudou, ele sempre tira 100 em complexidade/bugs/incidentes mesmo com 2 linhas alteradas. Score alto sem risco absoluto.
7. **`scoring.py` — dado ausente vira 0**: `test_health.get(module, 100.0)` e `flakiness.get(module, 0.0)` zeram o risco quando não há testes. Módulo sem cobertura parece seguro.
8. **`git_reader.py:resolve_comparison_base` — modo AUTO frágil**: usa `git describe` no `head.parents[0]`; em histórico com merge, a tag pode vir de branch lateral. Sem tags, volta ao primeiro commit — diff gigante e lento em repos grandes.
9. **`git_reader.py:get_changed_files` — `int(added_str)` sem try**: se `--numstat` retornar linha inesperada (binário com `-` tratado, mas rename com `-z` + path vazio), `ValueError("Saída Git incompleta")` aborta a análise inteira.
10. **`release_history.py` — `record_release_analysis` sem upsert**: reanalisar o mesmo intervalo cria snapshot duplicado; o resumo mostra só o mais recente, mas o banco cresce sem limite e filtros por módulo fazem `JOIN` cada vez mais caro.
11. **`app.py:release_trends` — `st.rerun()` após `record_release_outcome`**: recarrega a página inteira e perde `selected_release`/`selected_module` (keys fixas, mas `history` recarregado do zero), UX confusa.
12. **`app.py:publication_decision` — nome sem autenticação**: `st.text_input("Seu nome")` é só string declarada; qualquer pessoa registra "publicar" como outra pessoa. Auditoria fraca.
13. **Fuso fixo `America/Sao_Paulo` + formatação com vírgula**: `format_score`/`format_datetime_br` quebram reprocessamento se o CSV exportado for reimportado (ponto vs vírgula, ISO vs BR).
14. **`discover_quality_sources` ignora `sample_data` por nome**: se o produto real tiver pasta chamada `examples/` ou `fixtures/`, os XMLs legítimos são silenciosamente ignorados.
15. **`requirements.txt` sem pin (`streamlit>=1.32`, `pytest>=8.0`)**: CI pode quebrar com major nova; `junitparser` 4.x mudou API de `JUnitXmlError` usada no `except` do `app.py:930`.

## O que foi criado aqui a partir dessa análise

Um site **maior e intencionalmente bugado** inspirado no Garantiu, com os mesmos 7 conceitos + 2 telas extras (Login e Admin), nos dois stacks:

- `app_bugado.py` — Streamlit com 9 telas, 60+ bugs intencionais (SQL injection, XSS, shell=True, eval, pickle, path traversal, etc.)
- `garantiu_bugado/` — 10 módulos Python bugados espelhando os originais (scoring, git_reader, bug_history, incidents, release_history, test_reports, repository_source, test_execution, auth, api)
- `src/pages/` + `src/services/` — frontend React maior (Dashboard, ReleaseDetail, Login, Admin) com 40+ bugs de hooks, router, fetch e XSS
- `sample_data_bugado/` — CSVs/XMLs malformados de propósito
- `requirements-bugado.txt` — versões erradas/conflitantes de propósito

> ⚠️ Tudo aqui é propositalmente quebrado para treinar debug, code review e SAST. Não usar em produção.
