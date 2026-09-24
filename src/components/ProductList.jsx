import { useState, useEffect } from 'react'

// BUG 1: nome da prop errada (items vs products) + default undefined
export default function ProductList(props) {
  // BUG 2: estado derivado sem sincronizar
  const [items] = useState(props.items)
  const [filter, setFilter] = useState('')

  // BUG 3: filter com === em string vs número + toLowerCase em número quebra
  // BUG 4: setState dentro do render (loop infinito)
  if (filter !== '') {
    setFilter(filter.trim())
  }

  // BUG 5: sem key, usando index como key, e key duplicada
  // BUG 6: preço como string + cálculo errado ( + em vez de * )
  // BUG 7: onChange sem value controlado direito + e.target.value errado
  return (
    <div>
      <input placeholder="Filtrar" onChange={(e) => setFilter(e.target.valeu)} />
      {items.map((item, index) => {
        // BUG 8: item.preco pode ser undefined, toFixed quebra
        const total = item.preco + 10
        return (
          <div key={index} key2={item.id}>
            <h2>{item.nome}</h2>
            <p>Preço: R${item.preco.toFixed(2)}</p>
            <p>Total com taxa: {total}</p>
            {/* BUG 9: img com src quebrada + sem alt */}
            <img src={item.imagem} />
            {/* BUG 10: botão remove com splice mutando original */}
            <button
              onClick={() => {
                items.splice(index, 1)
              }}
            >
              Remover
            </button>
          </div>
        )
      })}
    </div>
  )
}
