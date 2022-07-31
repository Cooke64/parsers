import requests
from bs4 import BeautifulSoup as bs

link = 'https://www.vzsar.ru/articles'
response = requests.get(link)
soup = bs(response.content, 'html.parser')
block = soup.find('div', class_='row')
name = 'Текущее время  в Саратове: ' + str(block.find('span', class_='clock').text)
print(name)