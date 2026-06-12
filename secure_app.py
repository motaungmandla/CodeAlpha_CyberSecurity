from flask import Flask, request, render_template_string, escape
import sqlite3
import os

app = Flask(__name__)

# FIX 1: Use environment variables for secrets
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # FIX 2: Use Parameterized Queries to prevent SQLi
    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return "Login Successful!"
    return "Login Failed!"

@app.route('/profile')
def profile():
    name = request.args.get('name', 'Guest')
    # FIX 3: Sanitize/Escape user input to prevent XSS
    safe_name = escape(name)
    html = "<h1>Welcome to your profile, {{ name }}!</h1>"
    return render_template_string(html, name=safe_name)

if __name__ == '__main__':
    # FIX 4: Disable debug mode in production
    app.run(debug=False)
