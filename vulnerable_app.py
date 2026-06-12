from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded Secret Key
app.secret_key = "super_secret_password_123" 

# VULNERABILITY 2: SQL Injection
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # BAD: String concatenation in SQL query
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return "Login Successful!"
    return "Login Failed!"

# VULNERABILITY 3: Cross-Site Scripting (XSS)
@app.route('/profile')
def profile():
    name = request.args.get('name', 'Guest')
    # BAD: Rendering user input directly into HTML
    html = f"<h1>Welcome to your profile, {name}!</h1>"
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True) # VULNERABILITY 4: Debug mode in production
