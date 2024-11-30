from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3 as sq
from cars import CarAboutDB
import re


app = Flask(__name__)
app.secret_key = 'kgmsgkmllskgmes3iqk434'  # Убедитесь, что у вас есть секретный ключ для сессий.

def connect_db():
    conn = sq.connect('Cars.db')
    return conn

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

dbase = None

@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = CarAboutDB(db)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route('/')
def index():
    cars = dbase.get_cars()
    return render_template('index.html', cars=cars)

@app.route('/car_about/<name>', methods=["GET", "POST"])
def car_about(name):
    car = dbase.get_car_by_name(name)
    if car:
        if request.method == "POST":
            # Если была отправлена форма для тест-драйва
            car_name = request.form['car_name']
            # Добавляем машину в сессию "избранное"
            if 'favourites' not in session:
                session['favourites'] = []
            session['favourites'].append(car_name)
            session.modified = True
            return redirect(url_for('favourites'))

        car_data = {
            "name": car[0],
            "price": car[1],
            "description": car[2],
            "max_speed": car[3],
            "power": car[4],
            "engine": car[5],
            "title": car[6],
            "image": car[7],
        }
        return render_template('car_about.html', car=car_data)
    else:
        return "Автомобиль не найден", 404

@app.route('/favourites')
def favourites():
    favourites = session.get('favourites', [])  # Получаем список из сессии
    return render_template('favourites.html', favourites=favourites)


@app.route('/add_to_favourites/<car_name>', methods=['POST'])
def add_to_favourites(car_name):
    # Если избранное еще не создано, создаем его
    if 'favourites' not in session:
        session['favourites'] = []
    
    # Добавляем автомобиль, если его еще нет в списке
    if car_name not in session['favourites']:
        session['favourites'].append(car_name)
    
    # Сохраняем изменения в сессии
    session.modified = True
    return redirect(url_for('favourites'))


@app.route('/remove_from_favourites/<car_name>', methods=['POST'])
def remove_from_favourites(car_name):
    # Проверяем, есть ли список избранного в сессии
    if 'favourites' in session:
        try:
            # Удаляем автомобиль из списка
            session['favourites'].remove(car_name)
            session.modified = True
        except ValueError:
            pass  # Если автомобиля нет в списке, просто игнорируем
    return redirect(url_for('favourites'))




# Хэширование пароля
password = "mypassword"
hashed_password = generate_password_hash(password, method='pbkdf2:sha256')


# Проверка пароля
is_valid = check_password_hash(hashed_password, "mypassword")  # True



@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            error = 'Пароли не совпадают'
        elif len(password) < 6 or not any(char.isdigit() for char in password):
            error = 'Пароль должен быть не менее 6 символов и содержать хотя бы одну цифру'
        elif dbase.check_user_exists(email):
            error = 'Пользователь с таким email уже существует'
        else:
            password_hash = generate_password_hash(password)
            if dbase.add_user(email, password_hash):
                flash('Вы успешно зарегистрированы!', 'success')
                return redirect(url_for('authorize'))
            else:
                error = 'Ошибка регистрации, попробуйте позже'

    return render_template('registr.html', error=error)







@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    error = None  # Начальное значение ошибки - None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = dbase.get_user_by_email(email)
        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('profile'))
        else:
            error = 'Неверный email или пароль'  # Показываем ошибку только при POST

    return render_template('authorize.html', error=error)



@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/registr')
def registr():
    return render_template('registr.html')

import base64

@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True)
