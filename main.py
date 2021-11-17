import datetime
import time
import random

import requests
from bs4 import BeautifulSoup as bs

data = datetime.datetime.now()
timer = time.time()


# Получаем html страницы
def get_page(link):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, * / *;q = 0.8'
    }
    if requests.get(link, headers=headers).ok:
        return requests.request('GET', link).text
    else:
        return 'Нет ответа от сервера'


# Получаем ссылки на новости
def get_news_links(html):
    soup, links = bs(html, 'lxml'), []
    for link in soup.find_all('a'):
        if 'football/11' in link.get('href') and link.get('href').endswith('html'):
            links.append('https://www.sports.ru/' + link.get('href'))
    return links


# Получаем тайтлы и новости
def get_news(list_links):
    urls, news = list_links, []
    for url in urls:
        text = ''
        post = get_page(url)
        soup = bs(post, 'lxml')
        title = str(soup.title).replace('<title>', '').replace(' - Футбол - Sports.ru</title>', '')
        for p in soup.find_all(itemprop="articleBody"):
            text += p.get_text()
        news.append({title: text.strip()})
        time.sleep(random.randint(2, 5))
    return news


# Ищем актуальный поддомен для liveball.pro
def get_subdomain_url(url):
    google_list = get_page(url)
    soup, links = bs(google_list, 'lxml'), []
    for link in soup.find_all('a'):
        if '.liveball.pro' in link.get('href'):
            links.append(link.get('href').replace('://', '.').split('.')[1])
    return links[1][0] + max(map(lambda x: x[1:], links), key=int)


def main():
    # Запрашиваем контент новостей
    page = get_page('https://www.sports.ru/football/topnews/')
    print('Сервер вернул страницу sports.ru')

    # Собираем нужные ссылки на новости из файла
    news_links = get_news_links(page)
    print(f'Получил {len(news_links)} ссылок на новости')

    # Получаем тайтлы и новости
    news = get_news(news_links)

    # Получаем актуальный поддомен для парсинга ссылок на матчи
    subdomain = get_subdomain_url('https://www.google.com/search?q=site%3Aliveball.pro')
    print('Нашел актуальный поддомен - ', subdomain)

    # Запрашиваем контент матчей
    matches = get_page(f'https://{subdomain}.liveball.pro/matches/{data.year}-{data.month}-{data.day}')
    print('Сервер вернул страницу liveball.pro')
    print(
        f'Ссылка на страницу трансляций \nhttps://{subdomain}.liveball.pro/matches/{data.year}-{data.month}-{data.day}')

    # Время работы скрипта
    print()
    print(f'Время работы скрипта {round(time.time() - timer, 2)} сек.')


if __name__ == '__main__':
    main()
