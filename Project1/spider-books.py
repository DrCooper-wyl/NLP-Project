import requests
import json
from bs4 import BeautifulSoup
import threading

def crawl_desc(url: str) -> str:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    t_book = soup.find_all('p')[3]
    res = t_book.string
    # print(res)
    return res

def save_desc(book):
    # print(book[0])
    with open(r'test/{}.txt'.format(book[0]), 'w+', encoding='utf-8') as output_file:
        output = crawl_desc(book[1])
        if crawl_desc(book[1]) == None:
            output_file.write("")
        else:
            output_file.write(output)

if __name__ == '__main__':
    # start=time.time()
    with open('url.json', 'r') as input_file:
        book_list = json.load(input_file)
    for book in book_list:
        t=threading.Thread(target=save_desc,args=(book,))
        t.start()
    # print(time.time()-start)
