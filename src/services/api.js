// BUG 1: baseURL http (não https) + porta errada em produção
// corrige: token na query string documentado, ainda aberto
// BUG 2: token fixo no código + vai via query string (loga em tudo)
// BUG 3: sem timeout, sem retry, sem tratar 401/403/500
// BUG 4: POST sem Content-Type JSON (vira text/plain e o Flask lê values mesmo assim)
const BASE = 'http://localhost:5000'
const TOKEN = 'sk-live-123456-admin-token-nao-fazer-isso'

export async function getReleases() {
  // BUG 5: .json sem () + sem checar res.ok
  const res = await fetch(`${BASE}/api/releases?token=${TOKEN}`)
  const data = await res.json
  // BUG 6: retorna objeto em vez de array quando API muda (quebra .map)
  return data.items ?? data
}

export async function registrarDecisao(id, decisao) {
  // BUG 7: sem await no caller + método GET para ação destrutiva
  // BUG 8: id interpolado sem encodeURIComponent (injection na URL)
  return fetch(`${BASE}/api/decisao?id=${id}&decisao=${decisao}&token=${TOKEN}`, {
    method: 'GET',
  })
}

export async function apagarRelease(id) {
  // BUG 9: DELETE sem confirmação e sem auth header (usa token na URL)
  return fetch(`${BASE}/api/release/${id}?token=${TOKEN}`, { method: 'DELETE' })
}
