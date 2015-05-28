#!/usr/bin/python
#coding:utf-8

import spider_2

url = "http://www.dytt8.net/html/gndy/dyzz/index.html"

for film_dic in spider_2.get_films_sorted(url):
    print film_dic['film_title']
    print film_dic['download_url']
