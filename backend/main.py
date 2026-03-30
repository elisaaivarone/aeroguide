from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
import requests # Biblioteca para consumir APIs externas
from dotenv import load_dotenv
from google import genai
from database import initialize_database

# Carrega as chaves seguras
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
AVIATION_API_KEY = os.getenv("AVIATION_API_KEY")

ai_client = genai.Client(api_key=GOOGLE_API_KEY)

# Inicia o banco de dados
initialize_database()

app = FastAPI(title="AeroGuide Ops API", description="Hybrid Logistics & Radar System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def operational_panel():
    return {"mensagem": "AeroGuide Ops: Online Logistics & Briefing System."}

@app.get("/flights/{flight_number}")
def flight_briefing(flight_number: str):
    flight_number = flight_number.upper() # Garante que a busca seja sempre em maiúsculo
    
    # 1. (Banco SQL)
    connection = sqlite3.connect("aeroguide.db")
    cursor = connection.cursor()
    cursor.execute("SELECT origin, destination, status FROM flights WHERE flight_number = ?", (flight_number,))
    sql_result = cursor.fetchone()
    connection.close()

    origin = ""
    destination = ""
    status = ""
    information_source = ""
    operational_details = None # Variável para armazenar detalhes operacionais adicionais, caso sejam necessários para o briefing

    if sql_result:
        origin = sql_result[0]
        destination = sql_result[1]
        status = sql_result[2]
        information_source = "Internal Network (SQL)"
        # Simulação de uma estrutura JSON completa para os dados SQL.
        operational_details = {
            "flight_date": "Today",
            "flight_status": status,
            "departure": {"iata": origin, "terminal": "S/N", "gate": "S/N", "scheduled": "S/N"},
            "arrival": {"iata": destination, "terminal": "S/N", "gate": "S/N", "scheduled": "S/N"},
            "airline": {"name": "GOL Linhas Aéreas", "iata": "G3"}
        }
    
    else:
        # 2. Se não achou no SQL, busca no Radar Global (API Externa AviationStack)
        try:
            url = f"http://api.aviationstack.com/v1/flights?access_key={AVIATION_API_KEY}&flight_iata={flight_number}"
            response = requests.get(url)
            radar_data = response.json()

            # Verifica se a API externa encontrou o voo na lista de "data"
            if "data" in radar_data and len(radar_data["data"]) > 0:
                operational_details = radar_data["data"][0] # Pega o primeiro voo da lista
                origin = operational_details["departure"]["iata"]
                destination = operational_details["arrival"]["iata"]
                status = operational_details["flight_status"]
                information_source = "Global Radar (AviationStack)"
            else:
                return {"error": f"Flight {flight_number} not located neither in the internal network nor in the global radar."
                }
        
        except Exception as e:
            return {"error": "Failed to connect to the Global Radar."}

    # 3. A IA atua como Coordenadora e gera o Briefing baseado em quem entregou a informação (SQL ou API)
    try:
        prompt = f"""
        Act as an operational dispatcher of an airline. 
        We have flight {flight_number} departing from airport {origin} to {destination}. The current status is: '{status}'.
        Write a super short 1-paragraph briefing for the ground crew (baggage/fueling) and flight attendants.
        Use aviation technical terms, be direct, and give a clear instruction based on the status.
        """
        
        ai_response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        return {
            "information_source": information_source,
            "ai_briefing": ai_response.text,
            "details": operational_details #O React usará isso para o mapa e os detalhes.
        }
    except Exception as e:
        return {"erro": f"Ops! AI system unavailable: {str(e)}"}