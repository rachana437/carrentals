from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'cars.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if user == 'admin' and pwd == 'admin':
            session['user'] = user
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()
    return render_template('dashboard.html', cars=cars)

@app.route('/book/<int:car_id>', methods=['GET', 'POST'])
def book_car(car_id):
    if request.method == 'POST':
        name = request.form['name']
        days = request.form['days']
        cursor = get_db().cursor()
        cursor.execute("INSERT INTO bookings (car_id, customer_name, days) VALUES (?, ?, ?)", (car_id, name, days))
        get_db().commit()
        return redirect(url_for('dashboard'))
    return render_template('book_car.html', car_id=car_id)
