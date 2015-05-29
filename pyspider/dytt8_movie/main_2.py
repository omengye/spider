#!/usr/bin/python
#coding:utf-8

from spider_2 import Dytt8Spider

url = "http://www.dytt8.net/html/gndy/dyzz/index.html"

dytt8spider = Dytt8Spider()
content = dytt8spider.open_url(url)
films = dytt8spider.get_films(content)
films_url = dytt8spider.get_download_url(films)

for film_dic in films_url:
    print film_dic['film_title']
    print film_dic['download_url']
