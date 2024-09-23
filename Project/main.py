from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'secret_key'

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        height = request.form.get('height')
        weight = request.form.get('weight')
        gender = request.form.get('gender')

        # Check if any fields are empty
        if not all([username, name, password, confirm_password, height, weight, gender]):
            error_message = 'Please fill out all fields'
            return render_template('register.html', error=error_message)

        if password != confirm_password:
            # Handle password mismatch error
            error_message = 'Passwords do not match'
            return render_template('register.html', error=error_message)

        # Create a new user and store the data
        users[username] = {"name": name, "password": password, "workouts": [], "diets": [], "progress": [], "height": height, "weight": weight, "gender": gender}
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/admin', methods=['GET', 'POST'])
@app.route('/admin/dashboard', methods=['GET', 'POST'])
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
@app.route('/admin/users')
def admin_users():
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    return render_template('admin_users.html', users=users)

@app.route('/admin/workout-plans')
def admin_workout_plans():
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    return render_template('admin_workout_plans.html', users=users)

@app.route('/admin/diet-plans')
def admin_diet_plans():
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    return render_template('admin_diet_plans.html', users=users)

@app.route('/user')
def user_dashboard():
    if 'username' not in session:
        return redirect(url_for('login')) 
    username = session['username']
    user_data = users.get(username)
    return render_template('user.html', user=user_data)

@app.route('/profile')
def profile():
    username = session.get('username')
    if username:
        user = users.get(username)
        
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))
 

    
@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    username = session.get('username')
    if username:
        user = users.get(username)
        if request.method == 'POST':
            name = request.form.get('name')
            height = request.form.get('height')
            weight = request.form.get('weight')
            gender = request.form.get('gender')
            goal = request.form.get('goal')
            target_weight = request.form.get('target_weight')
            target_date = request.form.get('target_date')
            current_weight = request.form.get('current_weight')
            
            if name:
                user['name'] = name
            if height:
                user['height'] = height
            if weight:
                user['weight'] = weight
            if gender:
                user['gender'] = gender
            if goal:
                user['goal'] = goal
            if target_weight:
                user['target_weight'] = target_weight
            if target_date:
                user['target_date'] = target_date
            if current_weight:
                user['current_weight'] = current_weight
            
            return redirect(url_for('profile'))
        return render_template('edit_profile.html', user=user)
    else:
        return redirect(url_for('login'))
@app.route('/diet_plan')
def diet_plan():
    user = {'diet_plan': {'calorie_intake': 2000, 'protein': 100, 'carbohydrates': 200, 'fat': 50, 'meals': [{'name': 'Breakfast', 'calories': 500}, {'name': 'Lunch', 'calories': 600}, {'name': 'Dinner', 'calories': 700}]}}
    return render_template('diet_plan.html', user=user)

@app.route('/workout')
def workout():
    user = {'workout_plan': {'exercises': [{'name': 'Bench Press', 'sets': 3, 'reps': 8, 'weight': 100}, {'name': 'Squats', 'sets': 3, 'reps': 10, 'weight': 150}]}}
    return render_template('workout.html', user=user)
@app.route('/nav')
def nav():
    return render_template('nav.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)