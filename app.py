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
            created_at TEXT,
            closed_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM issues WHERE status != 'Closed'")
    issues = c.fetchall()
    conn.close()
    return render_template("index.html", issues=issues)

@app.route('/closed')
def closed_issues():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM issues WHERE status = 'Closed'")
    issues = c.fetchall()
    conn.close()
    return render_template("closed_issues.html", issues=issues)

@app.route('/add', methods=['GET', 'POST'])
def add_issue():
    if request.method == 'POST':
        data = (
            request.form['title'],
            request.form['description'],
            request.form['priority'],
            request.form['status'],
            request.form['assigned_to'],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            None  # closed_at starts as None
        )
        conn = get_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO issues (title, description, priority, status, assigned_to, created_at, closed_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', data)
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template("add_issue.html")

@app.route('/edit/<int:issue_id>', methods=['GET', 'POST'])
def edit_issue(issue_id):
    conn = get_connection()
    c = conn.cursor()

    if request.method == 'POST':
        new_status = request.form['status']
        closed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if new_
