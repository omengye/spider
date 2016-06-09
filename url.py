#!/usr/bin/python
#coding:utf-8

from FilmURLSpider import SpiderDytt8

url = "http://www.dytt8.net/html/gndy/dyzz/index.html"

dytt8spider = SpiderDytt8()
content = dytt8spider.openUrl(url)
films = dytt8spider.getFilms(content)
filmsUrl = dytt8spider.getDownloadUrl(films)

for film_dic in filmsUrl:
    print film_dic['film_title']
    print film_dic['download_url']
