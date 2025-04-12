from flask import Flask, render_template, request, redirect, url_for, session
from flask import jsonify
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Dummy user data
users = {
    'john': {
        'password': '1234',
        'email': 'john@example.com',
        'blocked': ['spam_user']
    }
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('settings'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users and users[uname]['password'] == pwd:
            session['username'] = uname
            return redirect(url_for('settings'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/settings', methods=['GET'])
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    user = users.get(username)

    if not user:
        return "User not found", 404

    return render_template(
        'settings.html',
        user=user,
        blocked_users=user.get('blocked', [])
    )

@app.route('/update_account', methods=['POST'])
def update_account():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    new_username = request.form['username']
    new_email = request.form['email']

    # Update user details
    users[username]['email'] = new_email

    # Update username key if changed
    if new_username != username:
        users[new_username] = users.pop(username)
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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
