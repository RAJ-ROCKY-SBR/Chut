from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration logic here
        return redirect(url_for('login'))
    return render_template('register.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Settings route
@app.route('/settings')
def settings():
    return render_template('settings.html')

# Search route
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip().lower()
    dummy_users = ['rocky', 'raj', 'sam', 'darksbr', 'admin']
    dummy_chats = ['chat with sam', 'raj messages', 'dark group']

    results = []
    if query:
        for item in dummy_users + dummy_chats:
            if query in item.lower():
                results.append(item)

    return render_template('search.html', query=query, results=results)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
