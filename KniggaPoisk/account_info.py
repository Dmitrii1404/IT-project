import hashlib
import sqlite3

def sign():
    conn = sqlite3.connect('my_database.db')
    cur = conn.cursor()
    cur.execute('''
       CREATE TABLE IF NOT EXISTS Users (
       name TEXT PRIMARY KEY,
       login TEXT NOT NULL,
       password TEXT NOT NULL
       )
       ''')
    conn.commit()
    print('Вы зарегестрированы?')
    i_want = input()
    if i_want == 'нет':
        # регистрация
        print('Имя:', end=' ')
        accaunt_name = input()
        print('Логин:', end=' ')
        login = hashlib.sha1(input().encode()).hexdigest()
        print('Пароль:', end=' ')
        password = hashlib.sha1((input()).encode()).hexdigest()
        cur.execute(f"""INSERT INTO users(name, login, password) 
              VALUES(?, ?, ?)""", (accaunt_name, login, password))
        conn.commit()
        print(f'login = {login}, password = {password} was write')

    # Вход в аккаунт
    print('Войдите в аккаунт')
    print('Логин:', end=' ')
    login = hashlib.sha1(input().encode()).hexdigest()
    print('Пароль:', end=' ')
    password = hashlib.sha1((input()).encode()).hexdigest()
    cur.execute("SELECT * FROM Users WHERE login = ?", (login,))
    result = cur.fetchone()
    if result != None and password == result[2]:
        print('Хорош, таких мы знаем')
    else:
        print('Ты кто такой, иди отсюда')
    conn.close()
    accaunt_name = result[0] if result != None else ''

    return accaunt_name