from flask import Flask, request, render_template_string, redirect, url_for
from markupsafe import escape
import sqlite3
import os

app = Flask(__name__)

# FIX 1: Use environment variables for secrets
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Initialize database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    # Add a test user
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                      ('admin', 'secure_password_123'))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # User already exists
    conn.close()

# ROOT ROUTE - Added to fix 404 error
@app.route('/')
def index():
    return '''
    <h1>🔐 Secure Coding Demo - Task 3</h1>
    <h2>Security Fixes Implemented:</h2>
    <ul>
        <li>✅ SQL Injection Prevention (Parameterized Queries)</li>
        <li>✅ XSS Prevention (Input Sanitization)</li>
        <li>✅ Secure Secret Key Management</li>
        <li>✅ Debug Mode Disabled</li>
    </ul>
    <h3>Test the Application:</h3>
    <ul>
        <li><a href="/profile?name=TestUser">Test Profile Page</a></li>
        <li><a href="/login">Test Login Page</a></li>
        <li><a href="/profile?name=<script>alert('XSS')</script>">Try XSS Attack (Should be blocked)</a></li>
    </ul>
    <hr>
    <h4>CodeAlpha Cyber Security Internship - Task 3</h4>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
            return f"<h1>✅ Login Successful!</h1><p>Welcome, {escape(username)}!</p><a href='/'>Go Back</a>"
        return "<h1>❌ Login Failed!</h1><p>Invalid credentials</p><a href='/login'>Try Again</a>"
    
    # GET request - show login form
    return '''
    <h2>Login Page</h2>
    <form method="POST">
        <label>Username: <input type="text" name="username"></label><br><br>
        <label>Password: <input type="password" name="password"></label><br><br>
        <button type="submit">Login</button>
    </form>
    <a href='/'>Go Back</a>
    '''

@app.route('/profile')
def profile():
    name = request.args.get('name', 'Guest')
    # FIX 3: Sanitize/Escape user input to prevent XSS
    safe_name = escape(name)
    html = """
    <h1>Welcome to your profile, {{ name }}!</h1>
    <p>This page is protected against XSS attacks.</p>
    <p>Try accessing: /profile?name=&lt;script&gt;alert('XSS')&lt;/script&gt;</p>
    <a href='/'>Go Back</a>
    """
    return render_template_string(html, name=safe_name)

if __name__ == '__main__':
    # Initialize database
    init_db()
    # FIX 4: Disable debug mode in production
    print("\n🔐 Secure Flask App Running on http://127.0.0.1:9090")
    print("📝 CodeAlpha Cyber Security Internship - Task 3\n")
    app.run(debug=False, port=9090)