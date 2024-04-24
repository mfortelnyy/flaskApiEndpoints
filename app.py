import sqlite3

import bcrypt

conn = sqlite3.connect("p1.sqlite")
cursor = conn.cursor()
# SQL query to create the users table
sql_query = '''CREATE TABLE users (
    username INTEGER,
    email TEXT,
    password TEXT
)'''
from flask import Flask, render_template, redirect, request, jsonify, session, render_template_string, url_for

from DBmanager import DB_FILE, app, init_db

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Set secret key for session management
app.config['SESSION_TYPE'] = 'filesystem'  # Configure session type



@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = hash_password(data.get('password'))

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users (username, email, password)
                          VALUES (?, ?, ?)''', (username, email, password))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered successfully'})
    # catch specific error
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: users.username" in str(e):
            return jsonify({'error': 'Username already exists'}), 400
        else:
            return jsonify({'error': 'Registration failed. Please try again later.'}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''SELECT password FROM users WHERE username=?''', (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        hashed_password = row[0]
        # Verify password during login
        if verify_password(password, hashed_password):
            session['username'] = username
            return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid username or password'}), 401


@app.route("/logout", methods=["POST"])
def logout():
    # Clear session
    session.pop('username', default=None)
    return jsonify({"message": "Logout successful"}), 200


@app.route("/upload-video", methods=["POST"])
def upload_video():
    # Handle video upload here
    file = request.files["video"]
    # Save the video file
    file.save("uploaded_videos/" + file.filename)
    return jsonify({"message": "Video uploaded successfully"}), 200


@app.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'POST':
        # Save the form data to the session object
        session['email'] = request.form['email_address']
        return redirect(url_for('get_email'))

    return """
        <form method="post">
            <label for="email">Enter your email address:</label>
            <input type="email" id="email" name="email_address" required />
            <button type="submit">Submit</button>
        </form>
        """


@app.route('/get_email')
def get_email():
    if 'email' in session:
        return render_template_string("<h1>Welcome {{ session['email'] }}!</h1>")
    else:
        return redirect(url_for('set_email'))


@app.route('/delete_email')
def delete_email():
    # Clear the email stored in the session object
    session.pop('email', default=None)
    return '<h1>Session deleted!</h1>'

# hash password before saving to the database
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Verify password during login
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)



if __name__ == "__main__":
    init_db()
    app.run()