import hashlib
import sqlite3
import account_info
#import search_by_name_films

def account():
    return account_info.sign()



if __name__ == '__main__':
    print('Что вы хотите сделать?')
    i_want = input().lower()
    if i_want == 'войти в аккаунт':
        print(account())
