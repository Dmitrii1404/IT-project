import hashlib
import sqlite3


def check_sumbol():
    str_ = input()
    if str_ == '':
        print('Ошибка, введена пустая строка, попробуйте заново')
        return check_sumbol()
    else:
        return str_


def registration(account_name='', login=''):
    conn = sqlite3.connect(r'C:\Users\Dmitrii\Desktop\KniggaPoisk\database\account_login.db')
    cur = conn.cursor()
    cur.execute('''
       CREATE TABLE IF NOT EXISTS Users (
       name TEXT PRIMARY KEY,
       login TEXT NOT NULL,
       password TEXT NOT NULL
       )
       ''')
    conn.commit()
    print('Регистрация')
    if account_name == '':
        print('Имя:', end=' ')
        account_name = check_sumbol()
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
        return registration(account_name, login)
    else:
        cur.execute(f"""INSERT INTO users(name, login, password) 
              VALUES(?, ?, ?)""", (account_name, login, password2))
        conn.commit()
        conn.close()
        print('Вы успешно зарегестрированы')
        return account_name


def login_():
    conn = sqlite3.connect(r'C:\Users\Dmitrii\Desktop\KniggaPoisk\database\account_login.db')
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
        account_name = result[0]
        conn.close()
        return account_name
    else:
        print('Логин или пароль неверен')
        conn.close()
        return login_


# def account_info(name):
#     conn = sqlite3.connect(r'C:\Users\Dmitrii\Desktop\KniggaPoisk\database\account_info.db')
#     cur = conn.cursor()
#     cur.execute(f'''
#            CREATE TABLE IF NOT EXISTS Users_info (
#            name TEXT PRIMARY KEY,
#            genre TEXT NOT NULL,
#            age TEXT NOT NULL,
#            )
#            ''')
