import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

colunas = [row[1] for row in cursor.execute("PRAGMA table_info(usuarios)").fetchall()]
print("Colunas atuais:", colunas)

if "tipo" not in colunas:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN tipo TEXT DEFAULT 'funcionario'")
    print("Coluna 'tipo' adicionada.")

if "ativo" not in colunas:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN ativo INTEGER DEFAULT 1")
    print("Coluna 'ativo' adicionada.")

if "ultimo_login" not in colunas:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN ultimo_login TIMESTAMP")
    print("Coluna 'ultimo_login' adicionada.")

if "criado_em" not in colunas:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN criado_em TIMESTAMP")
    print("Coluna criado_em adicionada.")

cursor.execute("UPDATE usuarios SET tipo = 'admin' WHERE id = 1")
print("Usuário 1 definido como admin.")

conn.commit()
conn.close()

print("\nPronto! Rode o app novamente.")