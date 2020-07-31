import requests

from bs4 import BeautifulSoup
def crawler():     
    url = 'http://www.banilaco.com/search/topSearch.do?search=Y&searchWord=%ED%81%B4%EB%A0%8C%EC%A7%95%EB%B0%A4'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    #select = soup.head.find_all('meta')
    #for meta in select:
    #    print(meta.get('content'))
    print(html.content)

crawler()

