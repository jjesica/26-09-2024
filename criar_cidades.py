import sqlite3

# Conectar ao banco de dados de cidades
conn = sqlite3.connect('cidades.db')
cursor = conn.cursor()

# Criar tabela de cidades se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS Cidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
''')

# Adicionar cidades de exemplo
cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba', 'Porto Alegre']
for cidade in cidades:
    cursor.execute("INSERT INTO Cidades (nome) VALUES (?)", (cidade,))
conn.commit()
conn.close()
