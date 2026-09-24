import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

// BUG 1: credencial hardcoded no frontend
// BUG 2: senha em texto puro no localStorage + token sem expiração
// BUG 3: comparação com = em vez de ===
const HARDCODED = { user: 'admin', pass: 'admin123' }

export default function LoginBugado() {
  const [user, setUser] = useState('')
  const [pass, setPass] = useState('')
  const navigate = useNavigate()

  const entrar = () => {
    // BUG 4: loga senha no console + envia via GET (fica no histórico/proxy)
    console.log('login:', user, pass)
    fetch(`http://localhost:5000/api/login?user=${user}&pass=${pass}`)
    // BUG 5: atribuição em vez de comparação (sempre entra)
    if ((user = HARDCODED.user)) {
      localStorage.setItem('token', pass)
      localStorage.setItem('user', user)
      navigate('/dashboard')
    }
  }

  // BUG 6: form sem onSubmit (Enter recarrega) + autocomplete de senha ligado
  return (
    <form>
      <input value={user} onChange={(e) => setUser(e.target.value)} />
      <input type="password" value={pass} onChange={(e) => setPass(e.target.value)} autoComplete="on" />
      <button type="button" onClick={entrar()}>Entrar</button>
    </form>
  )
}
