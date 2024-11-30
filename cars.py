import sqlite3 as sq

class CarAboutDB:
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()

    def create_table_cars(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS cars(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        description TEXT,
        max_speed INTEGER,
        power INTEGER,
        engine INTEGER,
        title TEXT,
        image BLOB
        )''')
        self.db.commit()

    def get_cars(self):
        try:
            self.cursor.execute('SELECT name, description, price, image FROM cars LIMIT 10')
            res = self.cursor.fetchall()
            if res:
                return res
        except sq.Error as e:
            print('Ошибка получения категории из БД ' + str(e))
        return False

    def get_car_by_name(self, name):
        """Получение данных об автомобиле по имени"""
        try:
            self.cursor.execute('SELECT name, price, description, max_speed, power, engine, title, image FROM cars WHERE name = ?', (name,))
            res = self.cursor.fetchone()
            if res:
                return res
        except sq.Error as e:
            print('Ошибка получения данных об автомобиле из БД: ' + str(e))
        return None

    def create_table_users(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL)''')
        self.db.commit()

    def add_user(self, first_name, last_name, e_mail, password):
        try:
            self.cursor.execute(
                'INSERT INTO users(first_name, last_name, email, password) VALUES(?, ?, ?, ?)',
                (first_name, last_name, e_mail, password))
            self.db.commit()
            return True
        except sq.IntegrityError as e:
            print('Ошибка: Данный email уже зарегистрирован. ' + str(e))
            return False
        except sq.Error as e:
            print('Ошибка подключения к БД: ' + str(e))
            return False

        
    def check_user_exists(self, email):
        try:
            self.cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            return self.cursor.fetchone() is not None
        except sq.Error as e:
            print('Ошибка при проверке пользователя: ' + str(e))
            return False


    def get_user_by_email(self, email):
        try:
            self.cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            return self.cursor.fetchone()
        except sq.Error as e:
            print('Ошибка при получении пользователя: ' + str(e))
            return None

    def add_user(self, e_mail, password):
        try:
            self.cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (e_mail, password))
            self.db.commit()
            return True
        except sq.Error as e:
            print(f'Ошибка при добавлении пользователя: {e}')
            return False

