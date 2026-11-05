import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, eur, login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "chave-secreta-para-projeto"
app.jinja_env.filters["eur"] = eur


def get_db_connection():
    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    conn = get_db_connection()

    totals = conn.execute(
        """
        SELECT 
            SUM(CASE WHEN type = 'receita' THEN amount ELSE 0 END) AS total_receitas,
            SUM(CASE WHEN type = 'despesa' THEN amount ELSE 0 END) AS total_despesas
        FROM transactions 
        WHERE user_id = ?
    """,
        (user_id,),
    ).fetchone()

    total_receitas = totals["total_receitas"] or 0.0
    total_despesas = totals["total_despesas"] or 0.0
    saldo = total_receitas - total_despesas

    transactions = conn.execute(
        """
        SELECT t.id, t.amount, t.type, t.description, t.date, c.name AS category
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = ?
        ORDER BY t.date DESC
        LIMIT 5
    """,
        (user_id,),
    ).fetchall()

    conn.close()
    return render_template(
        "index.html",
        saldo=saldo,
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        transactions=transactions,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("Preencha todos os campos", 400)
        if password != confirmation:
            return apology("As palavras-passe não coincidem", 400)

        conn = get_db_connection()
        existing_user = conn.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()

        if existing_user:
            conn.close()
            return apology("Nome de utilizador já existe", 400)

        hash_pw = generate_password_hash(password)
        conn.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            (username, hash_pw),
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("Introduza o utilizador e a palavra-passe", 400)

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if user is None or not check_password_hash(user["hash"], password):
            return apology("Utilizador ou palavra-passe incorretos", 400)

        session["user_id"] = user["id"]
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    conn = get_db_connection()

    if request.method == "POST":
        transaction_type = request.form.get("type")
        category_id = request.form.get("category_id")
        amount = request.form.get("amount")
        description = request.form.get("description")

        if (
            not transaction_type
            or not category_id
            or not amount
            or float(amount) <= 0
        ):
            conn.close()
            return apology("Dados de transação inválidos", 400)

        conn.execute(
            """
            INSERT INTO transactions (user_id, category_id, amount, type, description)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                session["user_id"],
                category_id,
                float(amount),
                transaction_type,
                description,
            ),
        )
        conn.commit()
        conn.close()

        return redirect("/")

    categories = conn.execute(
        "SELECT * FROM categories ORDER BY name"
    ).fetchall()
    conn.close()
    return render_template("add.html", categories=categories)


@app.route("/history")
@login_required
def history():
    conn = get_db_connection()
    transactions = conn.execute(
        """
        SELECT t.id, t.amount, t.type, t.description, t.date, c.name AS category
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.user_id = ?
        ORDER BY t.date DESC
    """,
        (session["user_id"],),
    ).fetchall()
    conn.close()

    return render_template("history.html", transactions=transactions)


if __name__ == "__main__":
    app.run(debug=True)
