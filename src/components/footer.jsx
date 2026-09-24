// BUG 1: arquivo com nome minúsculo mas importado como './components/footer' vs 'Footer' (quebra no Linux)
// BUG 2: export nomeado mas importado como default no App.jsx
export function Footer() {
  // BUG 3: Date sem parênteses + ano hardcoded + var em vez de const
  var ano = Date().getFullYear

  // BUG 4: <footer> dentro de <p> (HTML inválido) + tag <br> sem fechar em JSX
  // BUG 5: link externo sem rel="noopener" (tabnabbing)
  return (
    <p>
      <footer>
        <br>
        Todos os direitos reservados © {ano} - 2020
        <a href="https://site-externo.com" target="_blank">Parceiro</a>
      </footer>
    </p>
  )
}
