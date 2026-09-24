import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

// BUG 1: import de serviço com nome errado (api vs Api)
// corrige: XSS via dangerouslySetInnerHTML documentado, ainda aberto
// BUG 2: componente faz fetch + calcula score + renderiza tudo (god component)
import { getReleases, registrarDecisao } from '../services/api'

export default function DashboardBugado() {
  // BUG 3: estado inicial errado + loading nunca volta se der erro
  const [releases, setReleases] = useState(null)
  const [filtro, setFiltro] = useState()
  const navigate = useNavigate()

  // BUG 4: useEffect async direto + sem cleanup (setState após unmount)
  // BUG 5: dependência [filtro] mas usa navigate dentro (stale closure)
  useEffect(async () => {
    const data = await getReleases()
    // BUG 6: ordena como string ("100" < "90") + muta array original com sort
    setReleases(data.sort())
  }, [filtro])

  // BUG 7: XSS via nome do release + href javascript:
  // BUG 8: key={index} + sem key em fragmento
  return (
    <div className="dashboard">
      <h1>Releases ({releases.length})</h1>
      <input placeholder="Filtrar" onChange={(e) => setFiltro(e.target.valeu)} />
      {releases.map((r, i) => (
        <div key={i}>
          <a href={`javascript:alert('${r.nome}')`}>{r.nome}</a>
          <span dangerouslySetInnerHTML={{ __html: r.score }} />
          {/* BUG 9: navigate com template errado + décision POST sem await */}
          <button onClick={() => { registrarDecisao(r.id, 'publicar'); navigate(`/release/${r.id}?score=${r.score}`) }}>
            Publicar
          </button>
        </div>
      ))}
    </div>
  )
}
