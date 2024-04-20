import hashlib
import sqlite3


def check_sumbol():
    str_ = input()
    if str_ == '':
        print('Ошибка, введена пустая строка, попробуйте заново')
        return check_sumbol()
    else:
        return str_


def registration(username='', login=''):
    conn = sqlite3.connect(r'database\account_info.db')
    cur = conn.cursor()
    cur.execute('''
       CREATE TABLE IF NOT EXISTS Users (
       username TEXT PRIMARY KEY,
       login TEXT NOT NULL,
       password TEXT NOT NULL
       )
       ''')
    conn.commit()
    print('Регистрация')
    if username == '':
        print('Имя:', end=' ')
        username = check_sumbol()
        print('Логин:', end=' ')
        login = check_sumbol()
        login = hashlib.sha1(login.encode()).hexdigest()
    print('Пароль:', end=' ')
    password1 = check_sumbol()
    password1 = hashlib.sha1(password1.encode()).hexdigest()
    print('Введите пароль еще раз:', end=' ')
    password2 = hashlib.sha1(input().encode()).hexdigest()
    if password1 != password2:
        print('Ошибра, пароли не совпадают, попробуйте еще раз')
        conn.close()
        return registration(username, login)
    else:
        cur.execute(f"""INSERT INTO users(username, login, password) 
              VALUES(?, ?, ?)""", (username, login, password2))
        conn.commit()
        conn.close()
        print('Вы успешно зарегестрированы')
        return username


def login_():
    conn = sqlite3.connect(r'database\account_info.db')
    cur = conn.cursor()
    # Вход в аккаунт
    print('Вход в аккаунт')
    print('Логин:', end=' ')
    login = hashlib.sha1(input().encode()).hexdigest()
    print('Пароль:', end=' ')
    password = hashlib.sha1((input()).encode()).hexdigest()
    cur.execute("SELECT * FROM Users WHERE login = ?", (login,))
    result = cur.fetchone()
    if result != None and password == result[2]:
        print('Вы успешно зашли в аккаунт')
        username = result[0]
        conn.close()
        return username
    else:
        print('Логин или пароль неверен')
        conn.close()
        return login_()


def account_info(username):
    conn = sqlite3.connect(r'database\account_info.db')
    cur = conn.cursor()
    cur.execute('''
           CREATE TABLE IF NOT EXISTS Users_info (
           username TEXT PRIMARY KEY,
           likes_genre TEXT NOT NULL,
           age TEXT NOT NULL
           )
           ''')
    conn.commit()
    likes_genre = ''
    genres = ['биография',
             'боевик',
             'вестерн',
             'военный',
             'детектив',
             'документальный',
             'драма',
             'исторический',
             'комедия',
             'короткометражка',
             'криминал',
             'мелодрама',
             'мюзикл',
             'приключения',
             'семейный',
             'спорт',
             'триллер',
             'ужасы',
             'фантастика',
             'фэнтези']
    print('Какие жанры вы предпочитаете?')
    while True:
        genre = input().lower()
        if genre in genres:
            likes_genre += ',' + genre
        print('Еще какие то?')
        x = input().lower()
        if x == 'нет':
            break
    print('Введите ваш возраст:', end=' ')
    age = int(input())
    cur.execute(f"""INSERT INTO users_info(username, likes_genre, age) 
                  VALUES(?, ?, ?)""", (username, likes_genre, age))
    conn.commit()
    conn.close()
    return username
