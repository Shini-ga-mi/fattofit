from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'secret_key'

# Your Flask routes and logic below
# ...


# In-memory data store (Replace with a database for a real app)
users = {
    "user1": {"name": "Niraj", "password": "password", "workouts": [], "diets": [], "progress": []}
}
admin = {"username": "admin", "password": "adminpass"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == admin['username'] and password == admin['password']:
            session['admin'] = True
            return redirect(url_for('admin_panel'))
        elif username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('user_dashboard'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        username = request.form['username']
        exercise = request.form['exercise']
        sets = request.form['sets']
        reps = request.form['reps']
        rest_time = request.form['rest_time']
        diet = request.form['diet']
        calories = request.form['calories']
        
        if username in users:
            if exercise and sets and reps and rest_time:
                users[username]['workouts'].append({
                    "exercise": exercise, "sets": sets, "reps": reps, "rest_time": rest_time
                })
            if diet and calories:
                users[username]['diets'].append({
                    "diet": diet, "calories": calories
                })
        else:
            return "User not found."
    
    return render_template('admin.html', users=users)

@app.route('/user')
def user_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    user_data = users.get(username)
    return render_template('user.html', user=user_data)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
