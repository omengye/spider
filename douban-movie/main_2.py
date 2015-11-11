#!/usr/bin/python

from spider_2 import DoubanSpider

url="http://movie.douban.com/nowplaying/beijing/"

doubanspider = DoubanSpider()
content = doubanspider.open_url(url)
films_list = doubanspider.get_films(content)
films_sorted = doubanspider.sort_films(films_list)

for film_dic in films_sorted:
    print film_dic['film_name'], str(film_dic['points']), film_dic['film_stars']
