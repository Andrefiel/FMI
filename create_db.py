import sqlite3

# Caminho do banco de dados
db_path = 'monitoring_data.db'

# Conectar ao banco de dados (ou criar, se não existir)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Verificar se a tabela existe
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='monitoring_events';")
table_exists = cursor.fetchone()

if not table_exists:
    print("Tabela 'monitoring_events' não encontrada. Criando a tabela...")
    # Criar a tabela caso não exista
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS monitoring_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        file_name TEXT NOT NULL,
        user TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # Inserir dados de exemplo (opcional)
    cursor.execute('''
    INSERT INTO monitoring_events (event_type, file_name, user)
    VALUES
        ('Criação', 'example.txt', 'Usuario_1'),
        ('Alteração', 'example2.txt', 'Usuario_2'),
        ('Exclusão', 'example3.txt', 'Usuario_1');
    ''')

    # Salvar as alterações
    conn.commit()
    print("Tabela criada com sucesso!")

else:
    print("A tabela 'monitoring_events' já existe.")

# Fechar a conexão
conn.close()
