import sqlite3
conn = sqlite3.connect("PingPong.sqlite")
cursor = conn.cursor()
sql_query = "'" CREATE TABLE users (
    username integer
)
from flask import Flask, request, jsonify, session

from DBmanager import DB_FILE, app


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

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








@app.route("/upload-video", methods=["POST"])
def upload_video():
    # Handle video upload here
    file = request.files["video"]
    # Save the video file
    file.save("uploaded_videos/" + file.filename)
    return jsonify({"message": "Video uploaded successfully"}), 200

if __name__ == "__main__":
    init_db()
    app.run()