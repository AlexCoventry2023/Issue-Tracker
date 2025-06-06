from flask import Flask, render_template, request, redirect
from datetime import datetime
import os
import psycopg2

app = Flask(__name__)

# Get DB URL from environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# Initialize the PostgreSQL DB (create table if not exists)
def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id SERIAL PRIMARY KEY,
            title TEXT,
            description TEXT,
            priority TEXT,
            status TEXT,
            assigned_to TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM issues")
    issues = c.fetchall()
    conn.close()
    return render_template("index.html", issues=issues)

@app.route('/add', methods=['GET', 'POST'])
def add_issue():
    if request.method == 'POST':
        data = (
            request.form['title'],
            request.form['description'],
            request.form['priority'],
            request.form['status'],
            request.form['assigned_to'],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        conn = get_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO issues (title, description, priority, status, assigned_to, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', data)
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template("add_issue.html")

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
