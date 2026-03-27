import sqlite3

def iniciar_banco():
    # Conecta ao banco de dados 
    conexao = sqlite3.connect("aeroguide.db")
    cursor = conexao.cursor()

    # Cria a tabela focada em operações de voo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_voo TEXT NOT NULL,
            origem TEXT,
            destino TEXT,
            status TEXT
        )
    """)

    # Verifica se a tabela está vazia. Se estiver, cadastra os voos da nossa companhia
    cursor.execute("SELECT COUNT(*) FROM voos")
    if cursor.fetchone()[0] == 0:
        # Usando siglas IATA (GRU, SDU, BSB) para manter o padrão profissional da aviação
        malha_aerea = [
            ("G3-1520", "GRU", "SDU", "No Horário"),
            ("G3-2040", "BSB", "SSA", "Atrasado - Manutenção"),
            ("G3-1090", "CWB", "CGH", "Embarque Próximo")
        ]
        
        # Insere os dados na tabela
        cursor.executemany("INSERT INTO voos (numero_voo, origem, destino, status) VALUES (?, ?, ?, ?)", malha_aerea)
        conexao.commit() 

    conexao.close() 