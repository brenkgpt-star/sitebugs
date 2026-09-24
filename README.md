# SiteBugs 🐛 - Loja + Garantiu Bugado (INTENCIONALMENTE CHEIO DE BUGS)

> ⚠️ Este projeto foi criado de propósito com dezenas de erros para treinar debug, code review e ferramentas de análise estática.

## Parte 2 — Garantiu Bugado (site maior, baseado em bernardohorn/garantiu)

Análise real do repo original em `ANALISE-GARANTIU.md` (15 bugs/fragilidades captados).
Versão maior e bugada aqui:
- `app_bugado.py` — Streamlit 9 telas (Login + 7 do original + Admin), 30+ bugs. Rode com `streamlit run app_bugado.py`
- `garantiu_bugado/` — 10 módulos espelhando os originais, cada um com 10+ bugs (SQLi, RCE, SSRF, XXE, pickle, MD5, hardcoded secrets)
- `src/pages/` + `src/services/` — frontend React maior (Dashboard, ReleaseDetail, Login) com 20+ bugs
- `sample_data_bugado/` — CSVs/XMLs malformados
- `requirements-bugado.txt` — dependências impossíveis/conflitantes
- Instalar: `pip install -r requirements-bugado.txt` (vai falhar de propósito)

## Parte 1 — Loja bugada (React)

## Como rodar (vai quebrar mesmo)
```bash
npm install
npm run dev
```

## Lista de bugs intencionais (gabarito)

### `package.json`
1. `react@19` com `react-dom@18` (versões incompatíveis)
2. script `build` sem `tsc` / sem lint

### `vite.config.js`
3. `port: "3000"` como string, `host: "localost"` typo
4. `module.exports` misturado com ESM

### `index.html`
5. `<title>` sem fechar
6. `id="app"` mas `main.jsx` procura `root`
7. `<script src="/src/Main.jsx">` case-sensitive errado + sem `type="module"`
8. css aponta para `/src/style.css` (arquivo real é `styles.css`)

### `src/main.jsx`
9. `import App from './app.jsx'` minúsculo (quebra no Linux)
10. `createRoot` importado de `react-dom` em vez de `react-dom/client`
11. sem checar `null` do `getElementById`

### `src/App.jsx` (10+ bugs)
- `useState(null)` + `.map` em `null`
- `useEffect(async () => ...)` sem deps = loop infinito
- `setCount(count + 1)` dentro do effect
- `products.push` mutando estado
- `onClick={addProduct()}` executa na hora
- `count++` com stale state
- `==` + `mensagemSecreta` indefinida
- `class` em vez de `className`
- `dangerouslySetInnerHTML` com XSS
- falta `key` na lista, `Footer` importado errado

### `src/components/Header.jsx`
- `if ((menuOpen = true))` atribuição
- `user.nome` vs `user.name` + `.toUpperCase()` em undefined
- `cont.total` sendo que `cont` é número
- `<img>` sem `alt`, `<a href="#">` sem key

### `src/components/ProductList.jsx`
- `setFilter` dentro do render
- `e.target.valeu` typo
- `key={index}` + `key2` inválido
- `splice` mutando props
- `toFixed` em undefined

### `src/components/footer.jsx`
- export nomeado vs default
- `Date().getFullYear` sem `()`
- `<br>` sem fechar em JSX, `<footer>` dentro de `<p>`
- `target="_blank"` sem `rel="noopener"`

### `src/utils/api.js`
- `r.json` sem `()` , `res.data` de array
- `localStorage` sem `JSON.stringify/parse`
- `method: 'GET'` para delete
- token hardcoded + `eval` + URL com `${}` em aspas simples

### `src/styles.css`
- `width: 100` sem unidade, `#zzzzzz` inválido
- `@media (max-width 768px)` sem `:`
- `.topo` duplicado, `z-index: 9999999`

### `src/components/Cart.jsx`
- `props.total = 0` mutação
- `<!-- -->` dentro do JSX
- `100/0`, `setCart(null)` depois quebra `.length`
- `const limpar` depois do `return`

---
Feito para estudar. Não use em produção!
