import { useState } from 'react'
import './App.css'

function App() {
  const [flight, setFlight] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const searchFlight = async (searchNumber) => {
    if (!searchNumber) return;
    
    setLoading(true)
    setError('')
    setResult(null)
    setFlight(searchNumber)

    try {
      // Faz a requisição para a API Python
      const response = await fetch(`http://127.0.0.1:8000/voos/${searchNumber}`)
      const data = await response.json()

      // Verifica se a API Python retornou a chave de erro
      if (data.erro) {
        setError(data.erro)
      } else {
        setResult(data)
      }
    } catch (err) {
      console.error("Fetch Error:", err)
      setError("Connection failed. Please check if the Python server is running and CORS is configured.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <header className="header">
        <h1>✈️ AeroGuide Ops</h1>
        <p>Painel Integrado de Logística e Informações</p>
      </header>

      <main className="dashboard">
        <div className="search-container">
          <input 
            type="text" 
            placeholder="Digite o número do voo (e.g., LA3300)" 
            value={flight}
            onChange={(e) => setFlight(e.target.value)}
            className="input-flight"
          />
          <button onClick={() => searchFlight(flight)} className="btn-search">
            🔍 Search
          </button>
        </div>

        <div className="quick-buttons">
          <p>Voos Rápidos:</p>
          <button onClick={() => searchFlight('G3-1520')}>G3-1520</button>
          <button onClick={() => searchFlight('G3-2040')}>G3-2040</button>
          <button onClick={() => searchFlight('G3-1090')}>G3-1090</button>
        </div>

        {/* Status and Results Area */}
        {loading && <div className="loading">📡 Obtenção de dados de radar e geração de relatórios....</div>}
        
        {error && <div className="error">❌ {error}</div>}

        {result && (
          <div className="result-card">
            <div className="origin-badge">{result.origem_da_informacao}</div>
            <h2>Voo: {result.voo}</h2>
            <div className="info-grid">
              <div className="info-box">
                <span className="label">Rota</span>
                <span className="value">{result.rota}</span>
              </div>
              <div className="info-box">
                <span className="label">Status</span>
                <span className="value status-highlight">{result.status_sistema}</span>
              </div>
            </div>
            
            <div className="briefing-box">
              <h3>🤖 Resumo Operacional (AI):</h3>
              <p>{result.briefing_gerado_por_ia}</p>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App