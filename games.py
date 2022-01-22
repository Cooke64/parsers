import csv
import requests
from bs4 import BeautifulSoup

CSV = 'total.csv'
HOST = 'https://stopgame.ru/'
URL = 'https://stopgame.ru/review/new'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/'
              'avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.4.727 Yowser/2.5 Safari/537.36'
}


# Получаем страничку в html ввиде
def get_html(url, param=' '):
    req = requests.get(url, headers=HEADERS, params=param)
    req.encoding = 'utf-8'
    return req


# Выбираем необходимый контент со страницы, исспользуя find/get по классам или id
# Сохраняем все списком, исспользуя генератор списков
def get_cont(html):
    soup = BeautifulSoup(html.content, "html.parser")
    items = soup.find_all('div', class_='item article-summary')
    contain = [
        {
            'title': item.find('div', class_='caption caption-bold').get_text(strip=True),
            'date': item.find('div', class_='info').find('span', class_='info-item timestamp').get_text(strip=True),
            'link': HOST + item.find('div', class_='caption caption-bold').find('a').get('href'),
            'icon': item.find('a', class_='article-image image').find('img').get('src'),

        }
        for item in items
    ]
    return contain


# Сохраняем результаты в файл. Циклом проходим для записи всех элементов построчно
# Название колонок указываем произвольно
def save_res(items, path):
    with open(path, 'w', encoding="utf-8", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'date', 'link', 'icon2'])
        for item in items:
            writer.writerow([item['title'], item['date'], item['link'], item['icon']])


# Исследуем все страницы,если они имеются. Количество страниц выбираем сами.
# Для демонстрации процесса используется в цикле print, показывающий процесс иттерации
def get_info():
    PAG = int(input('Количество страниц для парсинга: '.strip()))
    html = get_html(URL)
    if html.status_code == 200:
        card = []
        for page in range(1, PAG + 1):
            print(f'Посмотрели {page} страницу')
            html = get_html(URL, param=str(page))
            card.extend(get_cont(html))
            save_res(card, CSV)
    else:
        print('error')


get_info()
