from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'asadsecret'

DB_FILE = 'jobs.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            date_applied TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    applications = conn.execute("SELECT * FROM applications ORDER BY date_applied DESC").fetchall()
    conn.close()
    return render_template('index.html', applications=applications)

@app.route('/add', methods=['POST'])
def add_application():
    company = request.form['company']
    position = request.form['position']
    date_applied = request.form['date_applied']
    status = request.form['status']
    notes = request.form['notes']

    conn = get_db_connection()
    conn.execute("INSERT INTO applications (company, position, date_applied, status, notes) VALUES (?, ?, ?, ?, ?)",
                 (company, position, date_applied, status, notes))
    conn.commit()
    conn.close()
    flash("Application added successfully!")
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_status(id):
    new_status = request.form['status']
    conn = get_db_connection()
    conn.execute("UPDATE applications SET status = ? WHERE id = ?", (new_status, id))
    conn.commit()
    conn.close()
    flash("Application status updated!")
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_application(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM applications WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Application deleted!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)