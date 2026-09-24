// BUG 1: URL hardcoded + sem .env
const API_URL = 'http://localhost:3000/produtos'

// BUG 2: sem try/catch, sem checar response.ok
// BUG 3: mistura async/await com .then + não retorna json direito
// BUG 4: localStorage sem JSON.parse seguro + sem checar null
export async function fetchProducts() {
  const cached = localStorage.getItem('produtos')
  if (cached) {
    return cached
  }

  const res = await fetch(API_URL).then((r) => r.json)
  const data = res.data

  // BUG 5: localStorage com objeto sem stringify + sem await necessário
  localStorage.setItem('produtos', data)

  // BUG 6: retorna undefined se data for undefined
  return data
}

// BUG 7: função delete usa GET em vez de DELETE + template string errada
// BUG 8: sem autenticação / token vazado no código
export function deleteProduct(id) {
  const TOKEN = 'sk-live-123456-admin-token-nao-fazer-isso'
  return fetch('http://localhost:3000/produtos/${id}?token=' + TOKEN, {
    method: 'GET'
  })
}

// BUG 9: eval + innerHTML (XSS crítico)
export function renderNome(nome) {
  return eval('"' + nome + '"')
}
