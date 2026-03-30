import { useState } from 'react'
import { MapContainer, TileLayer, Polyline, Marker, Popup } from 'react-leaflet'
import { DateTime } from 'luxon'
import L from 'leaflet'
import './App.css'

import iconUrl from 'leaflet/dist/images/marker-icon.png'
import iconShadowUrl from 'leaflet/dist/images/marker-shadow.png'
let DefaultIcon = L.icon({
  iconUrl,
  shadowUrl: iconShadowUrl,
  iconSize: [25, 41],
  iconAnchor: [12, 41]
})
L.Marker.prototype.options.icon = DefaultIcon

const airportCoords = {
  // Principais do Brasil
  'GRU': [-23.435, -46.473], 'SDU': [-22.910, -43.163], 'BSB': [-15.869, -47.917],
  'SSA': [-12.908, -38.322], 'CWB': [-25.531, -49.175], 'CGH': [-23.626, -46.656],
  'VCP': [-23.006, -47.134], 'CNF': [-19.624, -43.971], 'REC': [-8.125, -34.923],
  'POA': [-29.993, -51.171], 'FOR': [-3.776, -38.532], 'FLN': [-27.670, -48.552],
  'MAO': [-3.035, -60.049],  'BEL': [-1.379, -48.476],  'GIG': [-22.808, -43.243],
  'VIX': [-20.258, -40.286], 
  // Internacionais Populares
  'LAX': [33.94, -118.40], 'BOS': [42.36, -71.01], 'JFK': [40.64, -73.77],
  'MIA': [25.79, -80.28],  'MCO': [28.42, -81.31], 'LIS': [38.77, -9.13],
  'CDG': [49.00, 2.54],    'LHR': [51.47, -0.45],  'EZE': [-34.82, -58.53]
}

function App() {
  const [flight, setFlight] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const formatTime = (isoString) => {
    if (!isoString || isoString === 'S/N') return 'N/A';
    return DateTime.fromISO(isoString).toFormat('yyyy-MM-dd HH:mm:ss');
  }

  const searchFlight = async (searchNumber) => {
    if (!searchNumber) return;
    
    setLoading(true)
    setError('')
    setResult(null)
    setFlight(searchNumber)

    try {
      const response = await fetch(`https://aeroguide-v57i.onrender.com/flights/${searchNumber}`)
      const data = await response.json()

      if (data.error) {
        setError(data.error)
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
        <p>Integrated Logistics & Briefing Dashboard</p>
      </header>

      <main className="dashboard">
        <div className="search-container">
          <input 
            type="text" 
            placeholder="Enter flight number (e.g., LA3300)" 
            value={flight}
            onChange={(e) => setFlight(e.target.value)}
            className="input-flight"
          />
          <button onClick={() => searchFlight(flight)} className="btn-search">
            🔍 Search 
          </button>
        </div>

        <div className="quick-buttons">
          <p>Quick Flights:</p>
          <button onClick={() => searchFlight('G3-1520')}>G3-1520</button>
          <button onClick={() => searchFlight('G3-2040')}>G3-2040</button>
          <button onClick={() => searchFlight('G3-1090')}>G3-1090</button>
        </div>

        {loading && <div className="loading">📡 Fetching radar data and generating briefing...</div>}
        
        {error && <div className="error">❌ {error}</div>}

        {result && result.details && (
          <div className="result-card">
            
            <div className="flight-header-box">
              <div className="flight-name">
                <h2>Flight: {result.details.flight_iata || result.details.flight_number || flight.toUpperCase()}</h2>
                <span className="badge-source">{result.information_source}</span>
              </div>
              <div className="flight-route">
                <span className="iata">{result.details.departure?.iata?.toUpperCase() || 'N/A'}</span>
                <span className="arrow">→</span>
                <span className="iata">{result.details.arrival?.iata?.toUpperCase() || 'N/A'}</span>
              </div>
              <div className="flight-status">
                {result.details.flight_status ? result.details.flight_status.toUpperCase() : 'UNKNOWN'} (Operational)
              </div>
            </div>

            <div className="ops-panel">
              <div className="ops-box departure-box">
                <div className="ops-header">DEPARTURE</div>
                <div className="ops-iata">{result.details.departure?.iata?.toUpperCase() || 'N/A'}</div>
                
                <div className="ops-times-grid">
                  <div className="time-item">
                    <span className="time-label">SCHEDULED</span>
                    <span className="time-value">{formatTime(result.details.departure?.scheduled)}</span>
                  </div>
                  <div className="time-item">
                    <span className="time-label">ESTIMATED</span>
                    <span className="time-value highlighted">{formatTime(result.details.departure?.estimated)}</span>
                  </div>
                </div>

                <div className="ops-gates-grid">
                  <div className="gate-item">
                    <span className="gate-label">TERMINAL</span>
                    <span className="gate-value">{result.details.departure?.terminal || 'S/N'}</span>
                  </div>
                  <div className="gate-item">
                    <span className="gate-label">GATE</span>
                    <span className="gate-value">{result.details.departure?.gate || 'S/N'}</span>
                  </div>
                </div>
              </div>

              <div className="ops-box arrival-box">
                <div className="ops-header">ARRIVAL</div>
                <div className="ops-iata">{result.details.arrival?.iata?.toUpperCase() || 'N/A'}</div>
                
                <div className="ops-times-grid">
                  <div className="time-item">
                    <span className="time-label">SCHEDULED</span>
                    <span className="time-value">{formatTime(result.details.arrival?.scheduled)}</span>
                  </div>
                  <div className="time-item">
                    <span className="time-label">ESTIMATED</span>
                    <span className="time-value highlighted">{formatTime(result.details.arrival?.estimated)}</span>
                  </div>
                </div>

                 <div className="ops-gates-grid">
                  <div className="gate-item">
                    <span className="gate-label">TERMINAL</span>
                    <span className="gate-value">{result.details.arrival?.terminal || 'S/N'}</span>
                  </div>
                  <div className="gate-item">
                    <span className="gate-label">GATE</span>
                    <span className="gate-value">{result.details.arrival?.gate || 'S/N'}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="briefing-box">
              <h3>🤖 Operational Briefing (AI):</h3>
              <p>{result.ai_briefing}</p>
            </div>

            {/* Mapa operacional */}
            { result.details.departure?.iata && result.details.arrival?.iata && 
              airportCoords[result.details.departure.iata.toUpperCase()] && 
              airportCoords[result.details.arrival.iata.toUpperCase()] && (
              <div className="map-container-ops">
                <h3>Route Logistics Map</h3>
                <MapContainer 
                  center={airportCoords[result.details.departure.iata.toUpperCase()]} 
                  zoom={4} 
                  scrollWheelZoom={false}
                  className="map-leaflet"
                >
                  <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  />
                  <Marker position={airportCoords[result.details.departure.iata.toUpperCase()]}>
                    <Popup>Origin: {result.details.departure.iata.toUpperCase()}</Popup>
                  </Marker>
                  <Marker position={airportCoords[result.details.arrival.iata.toUpperCase()]}>
                    <Popup>Destination: {result.details.arrival.iata.toUpperCase()}</Popup>
                  </Marker>
                  <Polyline 
                    positions={[
                      airportCoords[result.details.departure.iata.toUpperCase()], 
                      airportCoords[result.details.arrival.iata.toUpperCase()]
                    ]} 
                    color="orange" 
                    weight={4} 
                    dashArray="10, 10" 
                  />
                </MapContainer>
              </div>
            )}
            
          </div>
        )}
      </main>
    </div>
  )
}

export default App