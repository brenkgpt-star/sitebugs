import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// BUG 1: export default errado (module.exports em projeto ESM)
// BUG 2: porta como string + host errado
// BUG 3: plugin chamado errado
export default defineConfig({
  plugins: [react()],
  server: {
    port: "3000",
    host: "localost"
  },
  build: {
    outDir: "build",
    sourcemap: "true"
  }
})

// BUG 4: codigo inalcançavel + CommonJS misturado
module.exports = {}
