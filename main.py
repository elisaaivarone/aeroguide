from fastapi import FastAPI
import sqlite3
import os
from dotenv import load_dotenv
from google import genai
from database import iniciar_banco

load_dotenv()

# Configuração da IA 
CHAVE_API = os.getenv("GEMINI_API_KEY")
cliente_ia = genai.Client(api_key=CHAVE_API)

# Inicia o banco de dados
iniciar_banco()

app = FastAPI(title="AeroGuide API")

@app.get("/")
def decolagem():
    return {"mensagem": "Bem-vinda ao AeroGuide API! Preparando para decolagem."}

@app.get("/destinos/{pais}")
def buscar_destino(pais: str):
    conexao = sqlite3.connect("aeroguide.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT capital, curiosidade_historica FROM destinos WHERE pais = ?", (pais,))
    resultado = cursor.fetchone()
    conexao.close()

    if resultado:
        return {
            "origem_dos_dados": "Banco de Dados Local (SQL)",
            "pais": pais,
            "capital": resultado[0],
            "historia_e_geografia": resultado[1]
        }
    
    # 2. Se não achou no SQL, usa a Inteligência Artificial!
    try:
        prompt = f"Atue como um guia de turismo especialista. Me diga qual é a capital de {pais} e uma breve curiosidade histórica ou geográfica fascinante sobre este país. Escreva no máximo dois parágrafos curtos."
        
        resposta_ia = cliente_ia.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        return {
            "origem_dos_dados": "Inteligência Artificial",
            "pais": pais,
            "dica_gerada_por_ia": resposta_ia.text
        }
    except Exception as e:
        return {"erro": "Ops! Não encontramos o destino no banco e a IA está descansando."}