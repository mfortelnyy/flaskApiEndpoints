import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_FILE = 'p1.db'


# db initialization
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Create users table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        email TEXT,
                        password TEXT
                    )''')
    conn.commit()
    conn.close()
