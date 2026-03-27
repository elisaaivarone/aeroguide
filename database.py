import sqlite3

# Função para iniciar o banco de dados e criar a tabela de voos
def initialize_database():
    connection = sqlite3.connect("aeroguide.db")
    cursor = connection.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_number TEXT NOT NULL,
            origin TEXT,
            destination TEXT,
            status TEXT
        )
    """)

    # Verifique se a tabela está vazia. Caso esteja, registre os voos da nossa empresa.
    cursor.execute("SELECT COUNT(*) FROM flights")
    if cursor.fetchone()[0] == 0:
        # Dados de exemplo para a malha interna da empresa
        flight_network = [
            ("G3-1520", "GRU", "SDU", "On Time"),
            ("G3-2040", "BSB", "SSA", "Delayed - Maintenance"),
            ("G3-1090", "CWB", "CGH", "Boarding Soon")
        ]
        
        # Insere os dados de voos da malha interna
        cursor.executemany("INSERT INTO flights (flight_number, origin, destination, status) VALUES (?, ?, ?, ?)", flight_network)
        connection.commit() 

    connection.close()