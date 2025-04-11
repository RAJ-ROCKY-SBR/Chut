from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key")

# Dummy users and block data
users = {
    "admin": {"password": "admin", "blocked": []}
}

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users and users[uname]['password'] == pwd:
            session['username'] = uname
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname not in users:
            users[uname] = {"password": pwd, "blocked": []}
            session['username'] = uname
            return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/settings')
def settings():
    if 'username' in session:
        return render_template('settings.html', username=session['username'], blocked=users[session['username']]['blocked'])
    return redirect(url_for('login'))

@app.route('/block/<user>')
def block_user(user):
    if 'username' in session and user in users:
        if user not in users[session['username']]['blocked']:
            users[session['username']]['blocked'].append(user)
    return redirect(url_for('settings'))

@app.route('/unblock/<user>')
def unblock_user(user):
    if 'username' in session and user in users[session['username']]['blocked']:
        users[session['username']]['blocked'].remove(user)
    return redirect(url_for('settings'))

@app.route('/search')
def search():
    if 'username' in session:
        query = request.args.get('q', '')
        matched_users = [u for u in users if query.lower() in u.lower() and u != session['username']]
        return render_template('search.html', results=matched_users, query=query)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # For local dev
    app.run(host='0.0.0.0', port=5000)
