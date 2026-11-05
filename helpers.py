from flask import redirect, render_template, session
from functools import wraps

def apology(message, code=400):
    """Exibe uma mensagem de erro ao utilizador."""
    return render_template("apology.html", top=code, bottom=message), code


def login_required(f):
    """
    Decora rotas para garantir que apenas utilizadores com sessão iniciada
    consigam aceder.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def eur(value):
    """Formata um número como moeda em Euros (€)."""
    if value is None:
        return "0,00 €"
    return f"{value:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
