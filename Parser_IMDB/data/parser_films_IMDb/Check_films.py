# перехожу по ссылкам на каждый сайт, собираю информацию и сохраняю в csv формате

import requests
from bs4 import BeautifulSoup
import fake_useragent
import json
import random
from time import sleep
import csv




with open("movie_URL_IMDb.json", "r", encoding="UTF-8") as file:
   all_films = json.load(file) # отсюда берем ссылки на саты фильмов, которые нужно спарсить

# with open("films.csv", "w", newline='', encoding="UTF-16") as file2:
#     writer = csv.writer(file2, delimiter="\t")
#     writer.writerow(
#         [
#             'Name',
#             'Runtime',
#             'Genres',
#             'Rating',
#             'Number of ratings',
#             'Description',
#             'Release date',
#             'Country',
#             'Budget',
#             'key words',
#             'Similars'
#
#         ]
#     )

count = 0
j = 650

for name, url in all_films.items():
    Run_time = ''  # Продолжительность фильма
    genres = []  # Жанры фильма
    rating = ''  # Рейтинг фильма
    number_of_ratings = ''  # Количество оценок
    description = ''  # Описание фильма
    Release_date = ''  # Дата релиза
    Country = []  # Страна
    Budget = ''  # бюджет фильма
    key_words = [] # Ключевые слова для фильма
    similars = [] # Похожие фильмы


    if count >= j and count < (j+550):

        user = fake_useragent.UserAgent().random  # Генерация user agent
        header = {"user-agent": user}  # Запись сгенерированного user agent
        f = list(url.split('/'))
        f = '/'.join(f[:5])
        responce = requests.get(f, headers=header).text  # Получение страницы и передача user agent
        soup = BeautifulSoup(responce, "lxml")  # типа подключаем парсер

        #description = soup.find_all('div', class_='ipc-html-content-inner-div')[1].text # Описание
        try:
            description = soup.find('span', class_='sc-466bb6c-0 hlbAws').text
        except:
            pass

        # responce = requests.get(f, headers=header).text
        # soup = BeautifulSoup(responce, "lxml")
        try:
            genres_html = soup.find_all('a', class_='ipc-chip ipc-chip--on-baseAlt')
            for genre in genres_html:
                genres.append(genre.text)
        except:
            pass

        try:
            rating = soup.find('span', class_='sc-bde20123-1 cMEQkK').text # Рейтинг
            rating = rating.replace('.', ',')
        except:
            pass

        try:
            number_of_ratings = soup.find('div', class_='sc-bde20123-3 gPVQxL').text # количество оценок
        except:
            pass

        try:
            some_info = soup.find_all('ul', class_='ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base')[1]
            some_info = some_info.find_all('li', class_='ipc-metadata-list__item')
        except:
            pass

        try:
            Release_date = some_info[0].find('a', class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link').text
        except:
            pass

        try:
            C = some_info[1].find_all('a', class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')
            for co in C:
                Country.append(co.text)
        except:
            pass

        try:
            Budget = soup.find_all('li', class_='ipc-metadata-list__item sc-1bec5ca1-2 bGsDqT')
            Budget = Budget[0].find('span', class_='ipc-metadata-list-item__list-content-item').text
        except:
            pass

        try:
            Run_time = soup.find('ul', class_='ipc-metadata-list ipc-metadata-list--dividers-none ipc-metadata-list--compact ipc-metadata-list--base')
            Run_time = Run_time.find('li', class_='ipc-metadata-list__item').find('div', class_='ipc-metadata-list-item__content-container').text
        except:
            pass

        try:
            similars_html = soup.find_all('div', class_='ipc-poster-card ipc-poster-card--base ipc-poster-card--dynamic-width ipc-sub-grid-item ipc-sub-grid-item--span-2')
            for s in similars_html:
                similar = s.find('a', class_='ipc-poster-card__title ipc-poster-card__title--clamp-2 ipc-poster-card__title--clickable').get('href')
                similars.append(similar)
        except:
            pass

        try:
            Name = soup.find('span', class_='hero__primary-text').text
        except:
            pass



        try:
            f = f + '/keywords'
            responce = requests.get(f, headers=header).text
            soup = BeautifulSoup(responce, "lxml")
            key_words_html = soup.find_all('div', class_='ipc-metadata-list-summary-item__tc')
            for word in key_words_html:
                key_words.append(word.text)  # сохранение ключевых слов
        except:
            pass

        count += 1

        print(f'Итерация номер {count}')

        with open("films.csv", "a", newline='', encoding="UTF-16") as file2:
            writer = csv.writer(file2, delimiter="\t")
            writer.writerow(
                [
                    Name,
                    Run_time,
                    ', '.join(genres),
                    rating,
                    number_of_ratings,
                    description,
                    Release_date,
                    ', '.join(Country),
                    Budget,
                    ', '.join(key_words),
                    ', '.join(similars)

                ]
            )


    else:
        if count < j:
            count += 1
        else:
            break





 # https://www.imdb.com/title/tt0111161/plotsummary/?ref_=tt_stry_pl
 # https://www.imdb.com/title/tt0111161/?ref_=sr_t_1

    # movies_menu = soup.find('div', id='dle-content')
    # description = movies_menu.find('div', class_='fdesc clearfix')  # Описание
    # try:
    #     description = description.find('span').text
    # except: description = None
    # movies_menu = movies_menu.find('div', class_='flists fx-row')
    #
    # try:
    #     g = movies_menu.find_all('ul', class_='flist')
    #
    #     h = movies_menu.find('ul', class_='flist flist-wide')
    #     h = h.find_all('li')
    #
    #     try:
    #         Name_ = g[0].find_all('li')[0].find_all('span')[1].text # Год релиза
    #     except: Name_ = None
    #     try:
    #         year = g[0].find_all('li')[1].find_all('span')[1].text # Год релиза
    #     except: year = None
    #     try:
    #         country = g[0].find_all('li')[2].find_all('span')[1].text # Страна
    #     except: country = None
    #     try:
    #         raitind = g[1].find('div', class_='frate frate-imdb').text.replace('.', ',') # Рейтинг IMDb
    #     except: raitind = None
    #     try:
    #         categori = h[0].find('span', itemprop='genre').text # Категории
    #     except: categori = None
    #     try:
    #         produser = h[1].find('span', itemprop='director').text  # Режисер
    #     except: produser = None
    #     try:
    #         actors = h[2].find('span', itemprop='actors').text  # Актеры
    #     except: actors = None
    #     print(url)
    #     print(raitind)
    #     with open(f"movies.csv", "a", newline='', encoding="UTF-16") as file2:
    #         writer = csv.writer(file2, delimiter="\t")
    #         writer.writerow(
    #             [
    #                 Name_,
    #                 description,
    #                 year,
    #                 country,
    #                 raitind,
    #                 categori,
    #                 produser,
    #                 actors,
    #                 url
    #             ]
    #         )
    # except:
    #     year = None
    #     country = None
    #     raitind = None
    #     categori = None
    #     produser = None
    #     actors = None
    # count += 1
    # print(f'Итерация {count}')
    # sleep(0.1)