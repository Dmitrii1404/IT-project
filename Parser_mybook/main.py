# Асинхронный парсер информации о фильмах IMDb, ссылки на которые расположены в файле
# Я лично считаю, что это имба. Имба на столько, что мне даже дали бан за слишком много запросов. Пришлось снизить обороты(((
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import fake_useragent
import json
import requests
import sqlite3

count_ = 0


async def fetch(session, url, headers=None):
    async with session.get(url, headers=headers) as response:
        # Задержка отправления, чтоб не забанил сайт (и мб это помогает прогрузить номально страницу)
        await asyncio.sleep(1)
        return await response.text()


async def parse_film(session, url, conn, cur, semaphore):
    global count_
    max = 100
    photo_url = ""

    ISBN = ""  # Код книги
    Name = ""  # Название
    Page = ""  # Количество страниц
    Age = ""  # Возрастное ограничение
    URL = ""  # Ссылка
    Runtime = ""  # Примерное время чтения
    Genres = []  # Жанры
    Topic = []  # Тема
    Rating = ""  # Оценка
    Number_of_ratings = ""  # Количество оценок
    Description = ""  # Описание
    Release_date = ""  # Дата выхода
    Author = ""  # Автор
    Similars = ""  # Похожие книги

    user = fake_useragent.UserAgent().random
    header = {"user-agent": user}
    URL = "https://mybook.ru/" + url
    cur.execute("SELECT * FROM books WHERE URL = ?", (url,))
    result = cur.fetchone()

    if (
        count_ <= max and result == None
    ):  # чтоб ноут долго не простаивал, парсинг разделяю на части, так что условие name <= max просто для моего удобства
        try:
            async with semaphore:
                html = await fetch(session, URL, headers=header)
            soup = BeautifulSoup(html, "lxml")
            count_ += 1
            print(f"Iteration: {count_}")

            try:
                some_info = soup.find("div", class_="ant-row sc-1c0xbiw-1 cyJjtq")
                Name = some_info.find("div", class_="m4n24q-0 hJyrxa").text
                some_info = some_info.find("div", class_="ant-col sc-1c0xbiw-9 eSjGMZ")
                Page = some_info.find_all("p", class_="lnjchu-1 dPgoNf")[0].text
                Age = some_info.find_all("p", class_="lnjchu-1 dPgoNf")[3].text
            except:
                pass

            try:
                some_info = soup.find("div", class_="ant-col sc-1c0xbiw-5 lotch")
                Rating = some_info.find("div", class_="sc-1s4c57r-0 goYpPi").text
                Number_of_ratings = some_info.find(
                    "div", class_="sc-1c0xbiw-6 cyZcfr"
                ).text
            except:
                pass

            try:
                some_info = soup.find("div", class_="iszfik-14 iSnZQd")
                some_info_1 = some_info.find_all("div", class_="iszfik-15 BerVK")[0]
                Release_date = some_info_1.find_all("dd", class_="iszfik-18 iEusfO")[
                    0
                ].text
                some_info_2 = some_info.find("div", class_="iszfik-15 BerVK")[1]
                ISBN = some_info_2.find_all("dd", class_="iszfik-18 iEusfO")[0].text
                Runtime = some_info_2.find_all("dd", class_="iszfik-18 iEusfO")[1].text
            except:
                pass

            try:
                some_info = soup.find_all("div", class_="sc-1sg8rha-0 gHinNz")
                some_info_1 = some_info[0].find_all("div", class_="sc-1sbv3y7-0 bQSldI")
                for genre in some_info_1:
                    Genres.append(genre.text)

                some_info_2 = some_info[1].find_all("div", class_="sc-1sbv3y7-0 bQSldI")
                for tp in some_info_2:
                    Topic.append(tp.text)
            except:
                pass

            try:
                some_info = soup.find("div", class_="iszfik-2 NZYdY")
                Description = some_info.text
            except:
                pass

            res = requests.get(
                photo_url, headers=header
            ).text  # Получение страницы и передача user agent
            soup = BeautifulSoup(res, "lxml")

            photo_ = soup.find_all("div", class_="sc-7c0a9e7c-2 ghbUKT")[0]
            img = photo_.find("img")

            try:
                imglink = img.get("srcset").split()[2]
                image = requests.get(imglink).content
                with open(r"imagine/" + h + ".jpg", "wb") as imgfile:
                    imgfile.write(image)
            except:
                imglink = img.get("src")
                print(imglink)
                image = requests.get(imglink).content
                with open(r"imagine/" + h + ".jpg", "wb") as imgfile:
                    imgfile.write(image)

            try:
                f = f + "/keywords"
                res = requests.get(
                    f, headers=header
                ).text  # Получение страницы и передача user agent
                soup = BeautifulSoup(res, "lxml")
                key_words_html = soup.find_all(
                    "div", class_="ipc-metadata-list-summary-item__tc"
                )
                for word in key_words_html:
                    key_words.append(word.text)  # Сохранение ключевых слов
            except Exception as e:
                print(f"Error parsing keywords for {name}: {e}")

            cur.execute(
                f"""INSERT INTO films(
                tag,
                Name,
                URL,
                Runtime,
                Genres,
                Rating,
                Number_of_ratings,
                Description,
                Release_date,
                Country,
                Budget,
                Director,
                Writer,
                Actors,
                key_words,
                Similars)
                              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    h,
                    Name,
                    URL_,
                    Run_time,
                    ", ".join(genres),
                    rating,
                    number_of_ratings,
                    description,
                    Release_date,
                    ", ".join(Country),
                    Budget,
                    Director,
                    Writer,
                    "; ".join(",".join(i) for i in Actors),
                    ", ".join(key_words),
                    ", ".join(similars),
                ),
            )
            conn.commit()

        except Exception as e:
            print(f"Error parsing {name}: {e}")

    elif count_ <= max:
        count_ += 1
        print(f"Книга с ссылкой {url} уже есть в дб")


async def main():
    semaphore = asyncio.Semaphore(
        10
    )  # Ограничение на количество одновременно выполняемых задач
    async with aiohttp.ClientSession() as session:
        with open("movie_URL_IMDb.json", "r", encoding="UTF-8") as file:
            all_films = json.load(file)

        conn = sqlite3.connect("books_info.db")
        cur = conn.cursor()
        cur.execute(
            """
               CREATE TABLE IF NOT EXISTS books (
               ISBN TEXT PRIMARY KEY,
               Name TEXT NOT NULL,
               Page TEXT NOT NULL,
               Age TEXT NOT NULL,
               URL TEXT NOT NULL,
               Runtime TEXT NOT NULL,
               Genres TEXT NOT NULL,
               Topic TEXT NOT NULL,
               Rating TEXT NOT NULL,
               Number_of_ratings TEXT NOT NULL,
               Description TEXT NOT NULL,
               Release_date TEXT NOT NULL,
               Author TEXT NOT NULL,
               Similars TEXT NOT NULL
               )
               """
        )
        conn.commit()
        tasks = []
        for url in all_films:
            tasks.append(parse_film(session, url, conn, cur, semaphore))

        await asyncio.gather(*tasks)

        conn.close()


async def run_main():
    await main()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_main())
