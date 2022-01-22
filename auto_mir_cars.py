import requests
from bs4 import BeautifulSoup
import csv
import os

LINK = 'https://avtomir.ru/used-cars/f/brand=125/'
FILE = 'cars.csv'
HOST = 'https://avtomir.ru'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.4.727 Yowser/2.5 Safari/537.36'
}


def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all('div', class_='card__desc')
    cars = []
    for item in items:
        cars.append(
            {
                'Название': item.find('a').text,
                'Пробег': item.find('div', class_='card__text card__text_ico-km').text.replace('Пробег:', ''),
                'Ссылка': HOST + item.find('a').get('href'),
                'Цена': item.find('span', class_='card__price-num').text + ' рублей.',
            }
        )
    return cars

def save(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Пробег', 'Ссылка', 'Цена'])
        for item in items:
            writer.writerow([item['Название'], item['Пробег'], item['Ссылка'], item['Цена']])
def parse():
    PAG = int(input('Количество страниц для парсинга: '.strip()))
    html = get_html(LINK)
    if html.status_code == 200:
        cars = []
        for page in range(1, PAG + 1):
            print(f'Geting {page}...')
            html = get_html(LINK, params={'page': str(page)})
            cars.extend(get_content(html.text))
        save(cars, FILE)
        print(f'Получена информация о {len(cars)} автомобилях. Все записано в {FILE}')
        os.startfile(FILE)
    else:
        print('error')


parse()
