from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Dummy user data
users = {
    'john': {'username': 'john', 'email': 'john@example.com', 'blocked': ['alice', 'bob']},
    # Add more users as needed
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username in users:
            session['username'] = username
            return redirect(url_for('settings'))
        else:
            return 'Invalid username'
    return render_template('login.html')

@app.route('/settings')
def settings():
    username = session.get('username')
    if username:
        user = users.get(username)
        blocked_users = user.get('blocked', [])
        return render_template('settings.html', user=user, blocked_users=blocked_users)
    else:
        return redirect(url_for('login'))

@app.route('/update_account', methods=['POST'])
def update_account():
    username = session.get('username')
    if username:
        user = users.get(username)
        new_username = request.form['username']
        new_email = request.form['email']
        user['username'] = new_username
        user['email'] = new_email
        return redirect(url_for('settings'))
    else:
        return redirect(url_for('login'))

@app.route('/unblock', methods=['POST'])
def unblock():
    username = session.get('username')
    if username:
        user = users.get(username)
        unblock_username = request.form['username']
        if unblock_username in user['blocked']:
            user['blocked'].remove(unblock_username)
        return redirect(url_for('settings'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
