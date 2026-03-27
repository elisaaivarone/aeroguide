from fastapi import FastAPI
import sqlite3
import os
import requests # Biblioteca para consumir APIs externas
from dotenv import load_dotenv
from google import genai
from database import iniciar_banco

# Carrega as chaves seguras
load_dotenv()
CHAVE_GOOGLE = os.getenv("GEMINI_API_KEY")
CHAVE_AVIATION = os.getenv("AVIATION_API_KEY")

cliente_ia = genai.Client(api_key=CHAVE_GOOGLE)

# Inicia o banco de dados
iniciar_banco()

app = FastAPI(title="AeroGuide Ops API", description="Sistema Híbrido de Logística e Radar")

@app.get("/")
def painel_operacional():
    return {"mensagem": "AeroGuide Ops: Sistema de Logística e Briefing online."}

@app.get("/voos/{numero_voo}")
def briefing_voo(numero_voo: str):
    numero_voo = numero_voo.upper() # Garante que a busca seja sempre em maiúsculo
    
    # 1. (Banco SQL)
    conexao = sqlite3.connect("aeroguide.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT origem, destino, status FROM voos WHERE numero_voo = ?", (numero_voo,))
    resultado_sql = cursor.fetchone()
    conexao.close()

    if resultado_sql:
        origem = resultado_sql[0]
        destino = resultado_sql[1]
        status = resultado_sql[2]
        origem_dado = "Malha Interna (SQL)"
    
    else:
        # 2. Se não achou no SQL, busca no Radar Global (API Externa AviationStack)
        try:
            url = f"http://api.aviationstack.com/v1/flights?access_key={CHAVE_AVIATION}&flight_iata={numero_voo}"
            resposta = requests.get(url)
            dados_radar = resposta.json()

            # Verifica se a API externa encontrou o voo na lista de "data"
            if "data" in dados_radar and len(dados_radar["data"]) > 0:
                voo_info = dados_radar["data"][0] # Pega o primeiro voo da lista
                origem = voo_info["departure"]["iata"]
                destino = voo_info["arrival"]["iata"]
                status = voo_info["flight_status"]
                origem_dado = "Radar Global Externa (AviationStack)"
            else:
                return {"erro": f"Voo {numero_voo} não localizado nem na malha interna, nem no radar global."}
        
        except Exception as e:
            return {"erro": "Falha ao conectar com o Radar Global."}

    # 3. A IA atua como Coordenadora e gera o Briefing baseado em quem entregou a informação (SQL ou API)
    try:
        prompt = f"""
        Atue como um despachante operacional de uma companhia aérea. 
        Temos o voo {numero_voo} indo do aeroporto {origem} para o {destino}. O status atual é: '{status}'.
        Escreva um briefing super curto de 1 parágrafo para a equipe de solo.
        Use termos de aviação, seja direto e dê uma instrução baseada no status.
        """
        
        resposta_ia = cliente_ia.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        return {
            "origem_da_informacao": origem_dado,
            "voo": numero_voo,
            "rota": f"{origem} -> {destino}",
            "status_sistema": status,
            "briefing_gerado_por_ia": resposta_ia.text
        }
    except Exception as e:
        return {"erro": f"Ops! Sistema da IA indisponível: {str(e)}"}