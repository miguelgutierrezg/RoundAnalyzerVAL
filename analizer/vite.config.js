// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/RoundAnalyzerVAL/',
  build: {
    outDir: '../docs', 
    emptyOutDir: true, 
  }
})
