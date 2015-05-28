#!/usr/bin/python

import spider_2

url="http://movie.douban.com/nowplaying/beijing/"
for film_dic in spider_2.get_films_sorted(url):
    print film_dic['film_name'], str(film_dic['points']), film_dic['film_stars']
