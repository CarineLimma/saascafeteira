import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS configuracoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_cafeteria TEXT NOT NULL,
    email_admin TEXT NOT NULL,
    senha_admin TEXT NOT NULL
)
""")



cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL DEFAULT 'funcionario',
    ativo INTEGER DEFAULT 1,
    ultimo_login TIMESTAMP,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")



cursor.execute("""
CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    tipo TEXT,
    descricao TEXT,
    valor REAL,
    data TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL
)
""")



cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    produto TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    total REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'Em preparo'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS reset_senha (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    token TEXT,
    expiracao TEXT
)
""")


try:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN tipo TEXT DEFAULT 'funcionario'")
    print("Coluna 'tipo' adicionada.")
except:
    print("Coluna 'tipo' já existe, pulando.")


try:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN ativo INTEGER DEFAULT 1")
    print("Coluna 'ativo' adicionada.")
except:
    print("Coluna 'ativo' já existe, pulando.")


cursor.execute("UPDATE usuarios SET tipo = 'admin' WHERE id = 1")

conn.commit()
conn.close()

print("Banco atualizado com sucesso!")
