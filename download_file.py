import requests
from bs4 import BeautifulSoup as bs

HOST = 'https://zastavok.net'
image_number = 0
# Переменная для опредления текущей страницы
page = 1
link = 'https://zastavok.net/funny/'
# Просим ввести нужное количество страниц для парсинга
N = int(input('Сколько сохранить страниц: '))
# Счетчик выполненной операции
count = 0
for storage in range(1, N + 1):  # Глобальный цикл для перехода по страницам
    response = requests.get(f'{link}/{page}')  # Показывает текущую страницу
    soup = bs(response.content, 'html.parser')
    block = soup.find_all('div', class_='short_full')
    for image in block:
        image_link = image.find('a').get('href')  # Получаем все ссылки на изображение в текущем блоке
        storage = requests.get(f'{HOST}{image_link}').text  # Переходим по ссылке и запускаем цикл парса на новой строке
        dow_soup = bs(storage, 'html.parser')
        down_block = dow_soup.find('div', class_='block_down')
        result = down_block.find('a').get('href')
        image = requests.get(f'{HOST}{result}').content  # Еще раз переходим по ссылке на скачивание нужного нам файла
        # download block image
        with open(f'img/{image_number}.jpg', 'wb') as file:
            file.write(image)
        image_number += 1  # Переменная для записи фото
        count += 1
    page += 1
    print(f'Total {count} things')
