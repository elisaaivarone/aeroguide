import sqlite3

def iniciar_banco():
    # Conecta ao banco (isso cria um arquivo chamado aeroguide.db na sua pasta)
    conexao = sqlite3.connect("aeroguide.db")
    cursor = conexao.cursor() # O cursor é quem "executa" os comandos SQL

    # Criação da tabela usando SQL 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS destinos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pais TEXT NOT NULL,
            capital TEXT,
            curiosidade_historica TEXT
        )
    """)

    # Verifica se a tabela está vazia. Se estiver, vamos inserir alguns dados.
    cursor.execute("SELECT COUNT(*) FROM destinos")
    if cursor.fetchone()[0] == 0:
        # Lista de destinos iniciais misturando geografia e história
        destinos = [
            ("Japao", "Tóquio", "O Japão é um arquipélago com mais de 6.800 ilhas, e Quioto foi a capital imperial por mais de mil anos."),
            ("Italia", "Roma", "A península itálica foi o berço do Império Romano, que dominou grande parte da Europa e do Mediterrâneo."),
            ("Egito", "Cairo", "Lar de uma das civilizações mais antigas do mundo, desenvolvida ao longo do rio Nilo.")
        ]
        
        # O comando INSERT coloca os dados na tabela
        cursor.executemany("INSERT INTO destinos (pais, capital, curiosidade_historica) VALUES (?, ?, ?)", destinos)
        conexao.commit() # Salva as alterações no banco

    conexao.close() # Fecha a conexão