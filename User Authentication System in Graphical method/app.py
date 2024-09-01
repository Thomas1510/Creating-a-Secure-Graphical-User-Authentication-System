from flask import Flask, render_template, redirect, request, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database setup (create table if it doesn't exist)
def setup_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Create Account route
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Save the account details to the database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('account_created'))
        except sqlite3.IntegrityError:
            flash('Account creation failed: Email already exists.', 'error')
        finally:
            conn.close()

    return render_template('create_account.html')

# Account Created route
@app.route('/account_created')
def account_created():
    return render_template('account_created.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verify login credentials
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            #flash('Login successful!', 'success')
            return redirect(url_for('welcome'))
        else:
            flash('Login failed: Incorrect email or password.', 'error')

    return render_template('login.html')

# Welcome route
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

# Run the Flask app
if __name__ == '__main__':
    setup_database()  # Ensure the database is set up
    app.run(debug=True)
