from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Dummy user data
users = {
    'john': {
        'username': 'john',
        'email': 'john@example.com',
        'password': '1234',
        'blocked': ['alice', 'bob']
    }
}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('settings'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('settings'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/settings')
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))

    current_user = users.get(session['username'])
    blocked_users = current_user.get('blocked', []) if current_user else []

    return render_template('settings.html', user=current_user, blocked_users=blocked_users)

@app.route('/update_account', methods=['POST'])
def update_account():
    if 'username' not in session:
        return redirect(url_for('login'))

    old_username = session['username']
    new_username = request.form['username']
    new_email = request.form['email']

    if old_username in users:
        users[old_username]['username'] = new_username
        users[old_username]['email'] = new_email
        if new_username != old_username:
            users[new_username] = users.pop(old_username)
            session['username'] = new_username

    return redirect(url_for('settings'))

@app.route('/unblock', methods=['POST'])
def unblock():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    to_unblock = request.form['username']
    if to_unblock in users[username]['blocked']:
        users[username]['blocked'].remove(to_unblock)

    return redirect(url_for('settings'))

if __name__ == '__main__':
    app.run(debug=True)
