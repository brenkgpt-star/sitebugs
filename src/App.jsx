import { useState, useEffect } from 'react'
import Header from './components/Header'
import ProductList from './components/ProductList'
import Footer from './components/footer'
import { fetchProducts } from './utils/api.js'

// BUG: componente gigante fazendo tudo (sem separação)
export default function App() {
  // BUG 1: estado inicial errado (null em vez de [])
  const [products, setProducts] = useState(null)
  const [count, setCount] = useState(0)
  const [user, setUser] = useState({ name: 'Visitante' })

  // BUG 2: useEffect sem array de dependências = loop infinito
  // BUG 3: async direto no useEffect + sem cleanup + setState após unmount
  useEffect(async () => {
    const data = await fetchProducts()
    setProducts(data)
    setCount(count + 1)
  })

  // BUG 4: useEffect com dependência errada (count causa loop)
  useEffect(() => {
    document.title = `Você tem ${products.length} produtos`
  }, [count])

  // BUG 5: mutação direta de estado
  const addProduct = () => {
    products.push({ id: Math.random(), name: 'Novo' })
    setProducts(products)
  }

  // BUG 6: == em vez de === + variável indefinida
  if (count == '0') {
    console.log(mensagemSecreta)
  }

  // BUG 7: acessar .map de null na primeira renderização
  // BUG 8: dangerouslySetInnerHTML com XSS + falta de key
  // BUG 9: onClick={funcao()} chama na hora em vez de passar referência
  // BUG 10: tag não fechada + class em vez de className
  return (
    <div class="app-container">
      <Header user={user} cont={count} />
      <h1>Loja Cheia de Bugs 🐛</h1>
      <button onClick={addProduct()}>Adicionar</button>
      <button onClick={() => setCount(count++)}>Incrementar</button>

      <div dangerouslySetInnerHTML={{ __html: user.name }} />

      <ul>
        {products.map((p) => (
          <li>{p.name} - R${p.preco}</li>
        ))}
      </ul>

      <ProductList items={products} />

      <Footer />
    </div>
  )
}
