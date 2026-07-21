from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    flash
)
import bcrypt
import sqlite3
import uuid
import time

from datetime import datetime

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

app = Flask(__name__)
app.secret_key = "cafeteria_secret_key_super_segura"

DB_PATH = "database.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT UNIQUE,
        senha TEXT
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
    CREATE TABLE IF NOT EXISTS reset_senha (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        token TEXT,
        expiracao TEXT
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

    conn.commit()
    conn.close()


init_db()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM usuarios WHERE email=?",
            (email,)
        ).fetchone()

        conn.close()

        if user and bcrypt.checkpw(
            senha.encode("utf-8"),
            user["senha"].encode("utf-8")
        ):
            session["user_id"] = user["id"]
            session["nome"] = user["nome"]
            return redirect(url_for("dashboard"))

        flash("Email ou senha inválidos!", "erro")

    return render_template("login.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        try:

            conn = get_db()

            senha_hash = bcrypt.hashpw(
                senha.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            conn.execute(
                """
                INSERT INTO usuarios (nome, email, senha)
                VALUES (?, ?, ?)
                """,
                (nome, email, senha_hash)
            )

            conn.commit()
            conn.close()

            flash("Administrador cadastrado com sucesso!", "sucesso")

            return redirect(url_for("login"))

        except Exception as e:

            flash("Erro ao cadastrar administrador!", "erro")

    return render_template("admin.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        try:
            conn = get_db()

            senha_hash = bcrypt.hashpw(
                senha.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            conn.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                (nome, email, senha_hash)
            )

            conn.commit()
            conn.close()

            flash("Conta criada com sucesso!", "sucesso")
            return redirect(url_for("login"))

        except Exception as e:
            flash("Email já cadastrado!", "erro")

    return render_template("registro.html")



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    transacoes = conn.execute(
        "SELECT * FROM transacoes WHERE usuario_id=? ORDER BY id DESC",
        (session["user_id"],)
    ).fetchall()

    entradas = conn.execute(
        "SELECT SUM(valor) as total FROM transacoes WHERE usuario_id=? AND tipo='entrada'",
        (session["user_id"],)
    ).fetchone()["total"] or 0

    saidas = conn.execute(
        "SELECT SUM(valor) as total FROM transacoes WHERE usuario_id=? AND tipo='saida'",
        (session["user_id"],)
    ).fetchone()["total"] or 0

    conn.close()

    return render_template(
        "dashboard.html",
        transacoes=transacoes,
        entradas=entradas,
        saidas=saidas,
        saldo=entradas - saidas
    )



@app.route("/add_transacao", methods=["POST"])
def add_transacao():
    if "user_id" not in session:
        return redirect(url_for("login"))

    tipo = request.form["tipo"]
    descricao = request.form["descricao"]
    valor = float(request.form["valor"])

    conn = get_db()

    conn.execute("""
        INSERT INTO transacoes (usuario_id, tipo, descricao, valor, data)
        VALUES (?, ?, ?, ?, ?)
    """, (
        session["user_id"],
        tipo,
        descricao,
        valor,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM transacoes WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


@app.route("/api/resumo")
def api_resumo():
    if "user_id" not in session:
        return jsonify({"erro": "não autorizado"})

    conn = get_db()

    entradas = conn.execute(
        "SELECT SUM(valor) as total FROM transacoes WHERE usuario_id=? AND tipo='entrada'",
        (session["user_id"],)
    ).fetchone()["total"] or 0

    saidas = conn.execute(
        "SELECT SUM(valor) as total FROM transacoes WHERE usuario_id=? AND tipo='saida'",
        (session["user_id"],)
    ).fetchone()["total"] or 0

    conn.close()

    return jsonify({
        "entradas": entradas,
        "saidas": saidas,
        "saldo": entradas - saidas
    })



@app.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    if request.method == "POST":
        email = request.form["email"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM usuarios WHERE email=?",
            (email,)
        ).fetchone()

        if not user:
            conn.close()
            flash("Email não encontrado!", "erro")
            return render_template("esqueci_senha.html")

    
        conn.execute(
            "DELETE FROM reset_senha WHERE email=?",
            (email,)
        )

        token = str(uuid.uuid4())
        expiracao = time.time() + 3600

        conn.execute(
            "INSERT INTO reset_senha (email, token, expiracao) VALUES (?, ?, ?)",
            (email, token, expiracao)
        )

        conn.commit()
        conn.close()

        flash(f"Link de reset: /reset/{token}", "sucesso")

    return render_template("esqueci-senha.html")


@app.route("/reset/<token>", methods=["GET", "POST"])
def reset(token):
    conn = get_db()

    dados = conn.execute(
        "SELECT * FROM reset_senha WHERE token=?",
        (token,)
    ).fetchone()

    if not dados:
        conn.close()
        return "Token inválido ou expirado"

    if float(dados["expiracao"]) < time.time():
        conn.close()
        return "Token expirado"

    if request.method == "POST":
        nova_senha = request.form["senha"]

        senha_hash = bcrypt.hashpw(
            nova_senha.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        conn.execute(
            "UPDATE usuarios SET senha=? WHERE email=?",
            (senha_hash, dados["email"])
        )

        conn.execute(
            "DELETE FROM reset_senha WHERE token=?",
            (token,)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("reset_senha.html")

@app.route("/redefinir-senha", methods=["GET", "POST"])
def redefinir_senha():

    if request.method == "POST":

        email = request.form["email"]
        nova_senha = request.form["senha"]

        try:

            conn = get_db()

            senha_hash = bcrypt.hashpw(
                nova_senha.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            conn.execute(
                """
                UPDATE usuarios
                SET senha = ?
                WHERE email = ?
                """,
                (senha_hash, email)
            )

            conn.commit()
            conn.close()

            flash("Senha redefinida com sucesso!", "sucesso")

            return redirect(url_for("login"))

        except:

            flash("Erro ao redefinir senha.", "erro")

    return render_template("redefinir-senha.html")

@app.route("/produtos")
def produtos():
    conn = get_db()
    products = conn.execute("SELECT * FROM produtos").fetchall()
    conn.close()
    return render_template("produtos.html", products=products)


@app.route("/add_product", methods=["POST"])
def add_product():
    nome = request.form.get("nome")
    preco = request.form.get("preco")

    if not nome or not preco:
        flash("Preencha todos os campos.", "erro")
        return redirect(url_for("produtos"))

    try:
        preco = float(preco)
    except ValueError:
        flash("Preço inválido.", "erro")
        return redirect(url_for("produtos"))

    conn = get_db()
    conn.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, preco))
    conn.commit()
    conn.close()

    flash("Produto adicionado com sucesso!", "sucesso")
    return redirect(url_for("produtos"))


@app.route("/delete_product/<int:id>")
def delete_product(id):
    conn = get_db()
    conn.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash("Produto excluído.", "sucesso")
    return redirect(url_for("produtos"))

@app.route("/pedidos", methods=["GET", "POST"])
def pedidos():
    conn = get_db()
    produtos = conn.execute("SELECT * FROM produtos").fetchall()

    if request.method == "POST":
        cliente = request.form.get("cliente")
        nome_produto = request.form.get("produto")
        quantidade = int(request.form.get("quantidade", 1))

        produto = conn.execute(
            "SELECT * FROM produtos WHERE nome = ?", (nome_produto,)
        ).fetchone()

        if not produto:
            flash("Produto não encontrado.", "erro")
            conn.close()
            return redirect(url_for("pedidos"))

        total = produto["preco"] * quantidade

        conn.execute(
            "INSERT INTO pedidos (cliente, produto, quantidade, total, status) VALUES (?, ?, ?, ?, ?)",
            (cliente, produto["nome"], quantidade, total, "Em preparo")
        )
        conn.commit()
        conn.close()

        flash("Pedido registrado com sucesso!", "sucesso")
        return redirect(url_for("pedidos"))

    todos_pedidos = conn.execute("SELECT * FROM pedidos ORDER BY id DESC").fetchall()

    total_pedidos = len(todos_pedidos)
    receita_total = sum(p["total"] for p in todos_pedidos)
    produtos_vendidos = sum(p["quantidade"] for p in todos_pedidos)
    conn.close()

    return render_template(
        "pedidos.html",
        pedidos=todos_pedidos,
        produtos=produtos,
        total_pedidos=total_pedidos,
        receita_total=f"{receita_total:.2f}",
        produtos_vendidos=produtos_vendidos
    )


@app.route("/pedidos/editar/<int:id>", methods=["GET", "POST"])
def editar_pedido(id):
    conn = get_db()
    pedido = conn.execute("SELECT * FROM pedidos WHERE id = ?", (id,)).fetchone()

    if request.method == "POST":
        status = request.form.get("status", pedido["status"])
        quantidade = int(request.form.get("quantidade", pedido["quantidade"]))

        produto = conn.execute(
            "SELECT * FROM produtos WHERE nome = ?", (pedido["produto"],)
        ).fetchone()
        total = produto["preco"] * quantidade if produto else pedido["total"]

        conn.execute(
            "UPDATE pedidos SET status = ?, quantidade = ?, total = ? WHERE id = ?",
            (status, quantidade, total, id)
        )
        conn.commit()
        conn.close()

        flash("Pedido atualizado!", "sucesso")
        return redirect(url_for("pedidos"))

    conn.close()
    return render_template("editar_pedido.html", pedido=pedido)


@app.route("/pedidos/deletar/<int:id>")
def deletar_pedido(id):
    conn = get_db()
    conn.execute("DELETE FROM pedidos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash("Pedido excluído.", "sucesso")
    return redirect(url_for("pedidos"))

@app.route("/configuracoes", methods=["GET", "POST"])
def configuracoes():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":

        acao = request.form.get("acao")

        if acao == "dados":

            nome_cafeteria = request.form["nome_cafeteria"]
            email_admin    = request.form["email_admin"]

            cursor.execute("SELECT * FROM configuracoes LIMIT 1")
            configuracao = cursor.fetchone()

            if configuracao:
                cursor.execute("""
                    UPDATE configuracoes
                    SET nome_cafeteria = ?, email_admin = ?
                    WHERE id = ?
                """, (nome_cafeteria, email_admin, configuracao["id"]))
            else:
                cursor.execute("""
                    INSERT INTO configuracoes (nome_cafeteria, email_admin, senha_admin)
                    VALUES (?, ?, '')
                """, (nome_cafeteria, email_admin))

            conn.commit()
            flash("Dados salvos com sucesso!", "sucesso")

        
        elif acao == "senha":

            senha_atual    = request.form.get("senha_atual", "")
            nova_senha     = request.form.get("nova_senha", "")
            confirmar      = request.form.get("confirmar_senha", "")

            usuario = conn.execute(
                "SELECT * FROM usuarios WHERE id = ?",
                (session["user_id"],)
            ).fetchone()

            
            if not bcrypt.checkpw(
                senha_atual.encode("utf-8"),
                usuario["senha"].encode("utf-8")
            ):
                flash("Senha atual incorreta.", "erro")
                conn.close()
                return redirect(url_for("configuracoes"))

            if len(nova_senha) < 8:
                flash("A nova senha precisa ter pelo menos 8 caracteres.", "erro")
                conn.close()
                return redirect(url_for("configuracoes"))

            if nova_senha != confirmar:
                flash("As senhas não coincidem.", "erro")
                conn.close()
                return redirect(url_for("configuracoes"))

            senha_hash = bcrypt.hashpw(
                nova_senha.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            conn.execute(
                "UPDATE usuarios SET senha = ? WHERE id = ?",
                (senha_hash, session["user_id"])
            )
            conn.commit()
            flash("Senha atualizada com sucesso!", "sucesso")

    cursor.execute("SELECT * FROM configuracoes LIMIT 1")
    configuracao = cursor.fetchone()
    conn.close()

    return render_template("configuracao.html", configuracao=configuracao)

@app.route("/cardapio")
def cardapio():

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM categorias ORDER BY nome")
        categorias = cursor.fetchall()

        cursor.execute("""
            SELECT *
            FROM produtos
            WHERE disponivel = 1
            ORDER BY nome
        """)
        produtos = cursor.fetchall()

    except Exception as erro:
        print(erro)
        categorias = []
        produtos = []

    finally:
        conn.close()

    return render_template(
        "cardapio.html",
        categorias=categorias,
        produtos=produtos
    )
@app.route("/usuarios", methods=["GET", "POST"])
def usuarios():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        tipo = request.form["tipo"]

        senha_hash = bcrypt.hashpw(
            senha.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        try:
            conn.execute(
                "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
                (nome, email, senha_hash, tipo)
            )
            conn.commit()
            flash("Usuário cadastrado com sucesso!", "sucesso")
        except:
            flash("Email já cadastrado!", "erro")

    usuarios = conn.execute(
        "SELECT id, nome, email, tipo FROM usuarios ORDER BY nome"
    ).fetchall()

    total_usuarios    = conn.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
    total_admins      = conn.execute("SELECT COUNT(*) FROM usuarios WHERE tipo='admin'").fetchone()[0]
    total_gerentes    = conn.execute("SELECT COUNT(*) FROM usuarios WHERE tipo='gerente'").fetchone()[0]
    total_funcionarios= conn.execute("SELECT COUNT(*) FROM usuarios WHERE tipo='funcionario'").fetchone()[0]

    conn.close()

    return render_template(
        "usuarios.html",
        usuarios=usuarios,
        total_usuarios=total_usuarios,
        total_admins=total_admins,
        total_gerentes=total_gerentes,
        total_funcionarios=total_funcionarios
    )

@app.route("/editar_usuario/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form.get("senha")
        tipo = request.form["tipo"]

        if senha:
            senha_hash = bcrypt.hashpw(
                senha.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            conn.execute("""
                UPDATE usuarios
                SET nome=?, email=?, senha=?, tipo=?
                WHERE id=?
            """, (nome, email, senha_hash, tipo, id))

        else:
            conn.execute("""
                UPDATE usuarios
                SET nome=?, email=?, tipo=?
                WHERE id=?
            """, (nome, email, tipo, id))

        conn.commit()
        conn.close()

        flash("Usuário atualizado com sucesso!", "sucesso")
        return redirect(url_for("usuarios"))

    usuario = conn.execute(
        "SELECT * FROM usuarios WHERE id=?", (id,)
    ).fetchone()

    conn.close()

    if usuario is None:
        flash("Usuário não encontrado.", "erro")
        return redirect(url_for("usuarios"))

    return render_template("editar_usuario.html", usuario=usuario)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )