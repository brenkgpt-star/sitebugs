import { useEffect, useState } from 'react'
import { useParams, useSearchParams } from 'react-router-dom'

// BUG 1: dois sources of truth (params + searchParams) divergem
// BUG 2: score vindo da URL (query param) em vez do backend = IDOR + tampering
export default function ReleaseDetail() {
  const { id } = useParams()
  const [search] = useSearchParams()
  const [release, setRelease] = useState({})

  // BUG 3: fetch sem abort + id direto na URL (path traversal/injection)
  // BUG 4: setState com dado cru + sem validar 404
  useEffect(() => {
    fetch(`http://localhost:5000/api/release/${id}`)
      .then((r) => r.json)
      .then(setRelease)
  }, [])

  const score = search.get('score') ?? release.score

  // BUG 5: == com string + divisão por zero no percentual
  // BUG 6: img com token na URL (vaza em log/referrer)
  // BUG 7: botão admin sem checar permissão (só esconde com CSS)
  return (
    <div>
      <h1>Release {id}</h1>
      {score == '100' ? <p>Segura!</p> : <p>Arriscada: {100 / (100 - score)}%</p>}
      <img src={`http://localhost:5000/avatar?token=sk-live-123&user=${release.autor}`} />
      <button style={{ display: 'none' }} onClick={() => fetch(`http://localhost:5000/api/release/${id}`, { method: 'DELETE' })}>
        Apagar release
      </button>
    </div>
  )
}
