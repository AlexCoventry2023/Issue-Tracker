from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "mydatabase"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "password"),
        cursor_factory=RealDictCursor
    )
    return conn

# Home page showing open tickets only
@app.route('/')
def index():
    conn = get_db_connection()
    issues = conn.execute("SELECT * FROM issues WHERE status != 'closed' ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template('index.html', issues=issues)

# View a single ticket
@app.route('/issue/<int:id>')
def issue(id):
    conn = get_db_connection()
    issue = conn.execute("SELECT * FROM issues WHERE id = %s", (id,)).fetchone()
    conn.close()
    return render_template('issue.html', issue=issue)

# Form to create a new ticket
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO issues (title, description, status, created_at) VALUES (%s, %s, %s, %s)',
            (title, description, 'open', created_at)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

# Update a ticket (status change)
@app.route('/update/<int:id>', methods=('POST',))
def update(id):
    new_status = request.form['status']
    closed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if new_status == 'closed' else None

    conn = get_db_connection()
    if closed_at:
        conn.execute(
            'UPDATE issues SET status = %s, closed_at = %s WHERE id = %s',
            (new_status, closed_at, id)
        )
    else:
        conn.execute(
            'UPDATE issues SET status = %s WHERE id = %s',
            (new_status, id)
        )
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Delete a ticket
@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM issues WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# View closed tickets
@app.route('/closed')
def closed_issues():
    conn = get_db_connection()
    issues = conn.execute("SELECT * FROM issues WHERE status = 'closed' ORDER BY closed_at DESC").fetchall()
    conn.close()
    return render_template('closed.html', issues=issues)


if __name__ == '__main__':
    app.run(debug=True)
