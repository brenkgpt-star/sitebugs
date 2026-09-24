import { useState } from 'react'

// BUG 1: props desestruturada errada (cont em vez de count, user pode ser undefined)
export default function Header({ user, cont }) {
  const [menuOpen, setMenuOpen] = useState(false)

  // BUG 2: comparação com = (atribuição) em vez de === 
  // BUG 3: variável windowlargura não definida
  if ((menuOpen = true)) {
    console.log('menu sempre aberto por causa do =')
  }

  // BUG 4: <a href="#"> recarrega página + img sem alt + sem key na lista
  // BUG 5: class em vez de className
  // BUG 6: setMenuOpen(!menuOpen) com estado stale (deveria ser callback)
  const links = ['Home', 'Produtos', 'Contato']

  return (
    <header class="topo">
      <img src="/logo.png" />
      {/* BUG 7: acessa user.nome (português) mas objeto tem user.name */}
      <p>Bem-vindo, {user.nome.toUpperCase()}</p>
      {/* BUG 8: mostra cont que é undefined se App passar errado */}
      <span>Carrinho: {cont.total}</span>
      <button onClick={() => setMenuOpen(!menuOpen)}>Menu</button>
      {menuOpen && (
        <nav>
          {links.map((l) => (
            <a href="#">{l}</a>
          ))}
        </nav>
      )}
    </header>
  )
}
