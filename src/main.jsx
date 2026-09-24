// BUG 1: import com case-sensitive errado (App vs app) e extensão errada
import App from './app.jsx'
// BUG 2: import React desnecessário + createRoot importado errado
import { createRoot } from 'react-dom'
import React from 'react'
import './styles.css'

// BUG 3: getElementById com id que não existe no index.html (root vs app)
const root = createRoot(document.getElementById('root'))

// BUG 4: render sem StrictMode e sem checar se root é null
root.render(<App />)
