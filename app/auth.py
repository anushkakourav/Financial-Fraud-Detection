from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from src.config import DATABASE_PATH


auth = Blueprint("auth", __name__)


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_user_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


# -----------------------
# SIGNUP
# -----------------------
@auth.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )

            conn.commit()

            flash("Account created successfully. Please login.", "success")
            return redirect(url_for("auth.login"))

        except sqlite3.IntegrityError:
            flash("Username already exists", "danger")

        finally:
            conn.close()

    return render_template("signup.html")


# -----------------------
# LOGIN
# -----------------------
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user"] = user["username"]

            return redirect(url_for("dashboard"))

        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")


# -----------------------
# LOGOUT
# -----------------------
@auth.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for("auth.login"))