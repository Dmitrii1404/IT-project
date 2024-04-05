import account_login

# import search_by_name_films

global name_account


def login():
    global name_account
    name_account = account_login.login_()
    return name_account


def registration():
    global name_account
    name_account = account_login.registration()
    return name_account


if __name__ == '__main__':
    while True:
        print('Что вы хотите сделать?')
        i_want = input().lower()
        if i_want == 'войти в аккаунт':
            print(login())
        elif i_want == 'зарегестрироваться':
            print(registration())
