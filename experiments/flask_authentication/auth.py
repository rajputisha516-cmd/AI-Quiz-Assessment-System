from flask import Flask, render_template, request, redirect
import sqlite3
import uuid

# Streamlit integration
import subprocess
import sys
import os
import time

app = Flask(__name__)

# =====================================================
# STREAMLIT PROCESS CONTROL (FIXED)
# =====================================================
streamlit_process = None

def start_streamlit():
    global streamlit_process

    if streamlit_process is None:
        # 🔥 CORRECT PATH: ROOT app.py
        streamlit_app_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../app.py")
        )

        streamlit_process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", streamlit_app_path],
            cwd=os.path.dirname(streamlit_app_path),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

# =====================================================
# DATABASE SETUP (UNCHANGED)
# =====================================================
def get_db():
    return sqlite3.connect("users.db")

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# =====================================================
# LOGIN (FIXED: TOKEN + STREAMLIT)
# =====================================================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            start_streamlit()
            time.sleep(2)  # allow Streamlit to boot

            token = str(uuid.uuid4())  # 🔑 token for Streamlit
            return redirect(f"http://localhost:8501/?token={token}")

        else:
            return "❌ Invalid credentials"

    return render_template("login.html")

# =====================================================
# SIGNUP (UNCHANGED)
# =====================================================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()
            return redirect("/")
        except:
            return "⚠️ User already exists"

    return render_template("signup.html")

# =====================================================
# LOGOUT (UNCHANGED)
# =====================================================
@app.route("/logout")
def logout():
    global streamlit_process
    if streamlit_process:
        streamlit_process.terminate()
        streamlit_process = None
    return redirect("/")

# =====================================================
# RUN FLASK
# =====================================================
if __name__ == "__main__":
    app.run(debug=True)
