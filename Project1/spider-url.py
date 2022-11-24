import requests
import json
from bs4 import BeautifulSoup


def crawl_url(url: str) -> [(str, str)]:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    t_book_list = soup.find_all('article', 'product_pod')
    t_book_list = [book.find_all('h3')[0].find_all('a')[0] for book in t_book_list]
    book_list = [(book['title'].replace('<','').replace('>','').replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('<',''),'https://books.toscrape.com/catalogue/{}'.format(book['href'])) for book in t_book_list]
    # print(t_book_list[0]['title'])
    return book_list


if __name__ == '__main__':
    url_list = ['https://books.toscrape.com/catalogue/page-{}.html'.format(i) for i in range(1, 11)]
    res = []
    for url in url_list:
        book_list = crawl_url(url)
        for book in book_list:
            res.append(book)
    res = json.dumps(res)
    with open('url.json', 'w+',encoding='utf-8') as outfile:
        outfile.write(res)
