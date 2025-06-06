from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('issues.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY,
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
    conn = sqlite3.connect('issues.db')
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
        conn = sqlite3.connect('issues.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO issues (title, description, priority, status, assigned_to, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template("add_issue.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
