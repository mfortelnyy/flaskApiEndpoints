import os
import sqlite3
import subprocess

import DBmanager

from DBmanager import DB_FILE, app

from flask import Flask, request, jsonify, session

app = Flask(__name__)

# ESTABLISH CONNECTION WITH A DATABASE
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    print(username)
    email = data.get('email')
    password = data.get('password')
    DBmanager.init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (username, email, password)
                      VALUES (?, ?, ?)''', (username, email, password))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User registered successfully'})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users WHERE username=? AND password=?''', (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


@app.route("/logout", methods=["POST"])
def logout():
    # Clear session
    session.clear()
    return jsonify({"message": "Logout successful"}), 200


def allowed_file(filename, ALLOWED_EXTENSIONS=['mp4']):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_video():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    # when user does not select file, browser also
    # return nice error
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        username = request.form.get('username')
        filename = f"{username}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Run the analyzer command
        analyzed_filename = f"analyzed_{filename}"
        analyzed_filepath = os.path.join(app.config['ANALYZED_FOLDER'], analyzed_filename)
        subprocess.run(['fmo', 'fmo-desktop', '--input', filepath, '--demo', analyzed_filepath])

        return jsonify({'message': 'File uploaded and analyzed successfully', 'filename': analyzed_filename})
    else:
        return jsonify({'error': 'File type not allowed'})


if __name__ == "__main__":
    DBmanager.init_db()
    app.run()
