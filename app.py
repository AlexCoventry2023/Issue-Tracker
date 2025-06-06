from flask import Flask, render_template, request, redirect
from datetime import datetime
import os
import psycopg2

app = Flask(__name__)

# Reusable PostgreSQL connection function
def get_connection():
    return psycopg2.connect(os.environ.get("postgresql://issue_tracker_db_297y_user:2LrHcy6UGkOCCeaHL9AzwCoSNIMfgnmP@dpg-d11mqvogjchc73864to0-a/issue_tracker_db_297y"))

# Initialize the PostgreSQL DB (run on app start)
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

# Homepage route — show all issues
@app.route('/')
def index():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM issues")
    issues = c.fetchall()
    conn.close()
    return render_template("index.html", issues=issues)

# Add issue route
@app.route('/add', methods=['GET', 'POST'])
def add_issue():
    if request.method == 'POST':
        da
