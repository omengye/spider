import bs4
import urllib.request
import re


UA = 'User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36'

headers = {
    'User-Agent': 'UA'
}

url = "http://www.dytt8.net/html/gndy/dyzz/index.html"

films = []

opener = urllib.request.build_opener()
opener.add_handler=headers
content = opener.open(url).read().decode('gbk')
soup = bs4.BeautifulSoup(content)

if soup.findAll('a', {'class': 'ulink'}):
    ulink = soup.findAll('a', {'class': 'ulink'})
else:
    js = soup.findAll('script', {'language': 'javascript'})[0].string
    pick_js = js[11:-22] # 挑出js部分
    fix_js = pick_js.replace('url=', '')
    urls = fix_js.split(';')
    url = ''
    for i in range(len(urls)):
        url = eval(urls[i])
    url = "http://www.dytt8.net" + url
    content = opener.open(url).read().decode('gbk')
    soup = bs4.BeautifulSoup(content)
    ulink = soup.findAll('a', {'class': 'ulink'})

def get_dytt8_films():

    for film_link in ulink:
        film = {}

        film_href = 'http://www.dytt8.net' + film_link['href']

        film['film_href'] = film_href

        film_content = opener.open(film_href).read().decode('gbk', 'ignore').encode('utf-8')

        film_soup = bs4.BeautifulSoup(film_content)

        title_all = film_soup.findAll('div', {'class': 'title_all'})

        if title_all:

            film['film_title'] = title_all[-1].h1.font.string

            film['download_url'] = film_soup.findAll('td', {'style': 'WORD-WRAP: break-word'})[0].a['href']
        else:
            break

        films.append(film)

    return films



dytt8_films = get_dytt8_films()
print(dytt8_films)