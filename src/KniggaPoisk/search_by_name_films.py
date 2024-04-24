# Здесь я реализую поиск фильмов по названию, то есть поисковик

import csv

print("прив")
input()
# Здесь указать базу данных, где расположенны фильмы
with open(
    r"C:\Users\Dmitrii\Desktop\project it\data\data_base_films\films_info_IMDb.csv",
    "r",
    encoding="UTF-16",
) as file:
    reader_object = csv.reader(file, delimiter="\t")
    count_ = 0
    dict_ = {}  # Сюда сохраняем результаты поиска

    x = input().lower()  # Ввод запроса

    for line in reader_object:
        count_ += 1
        l = line[1]
        l = l.lower()
        # Здесь будем просто сравнивать посимвольно и считать совпадения
        if x[0] in l:
            all_index = [str(i) for i, y in enumerate(l) if y == x[0]]
            c = 0
            for i in all_index:
                d = 0
                s = int(i)
                count = 0
                while d < len(x) and s < len(l):
                    if x[d] == l[s]:
                        count += 1
                    d += 1
                    s += 1
                c = max(c, count)
            if c >= (int(len(x) * 0.5) + 1):
                if c in dict_.keys():
                    dict_[c] += [l]
                else:
                    dict_[c] = [l]

    print(dict_)
