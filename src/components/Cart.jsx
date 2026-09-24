import { useState } from 'react'

// BUG 1: componente nunca usado, mas com loop infinito
// BUG 2: props mutada diretamente
export default function Cart(props) {
  props.total = 0

  // BUG 3: useState com objeto mas atualiza como número
  const [cart, setCart] = useState({ items: [] })

  // BUG 4: função definida depois do return (hoisting confuso com const)
  // BUG 5: divisão por zero + NaN
  return (
    <div>
      <h2>Carrinho: {cart.items.length}</h2>
      <button onClick={() => setCart(cart.items.length + 1)}>Add</button>
      <button onClick={() => limpar()}>Limpar</button>
      <p>Total: {100 / 0}</p>
      {/* BUG 6: comentário HTML dentro do JSX quebra */}
      <!-- comentario errado -->
    </div>
  )

  const limpar = () => {
    setCart(null)
  }
}
