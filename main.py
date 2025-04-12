from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy users data
users = {
    'testuser': {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass',
        'blocked': ['blockeduser1', 'blockeduser2']
    }
}

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', user=users[session['username']])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/settings', methods=['GET'])
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user = users[username]
    blocked_users = user.get('blocked', [])
    return render_template('settings.html', user=user, blocked_users=blocked_users)

@app.route('/update_account', methods=['POST'])
def update_account():
    if 'username' in session:
        username = session['username']
        users[username]['username'] = request.form['username']
        users[username]['email'] = request.form['email']
        return redirect(url_for('settings'))
    return redirect(url_for('login'))

@app.route('/unblock', methods=['POST'])
def unblock():
    if 'username' in session:
        username = session['username']
        unblock_user = request.form['username']
        if unblock_user in users[username]['blocked']:
            users[username]['blocked'].remove(unblock_user)
        return redirect(url_for('settings'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
