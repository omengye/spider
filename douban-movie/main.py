#!/usr/bin/python

from spider import DoubanSpider

url="http://movie.douban.com/"

doubanspider = DoubanSpider()
content = doubanspider.open_url(url)
films_dic = doubanspider.get_films(content)
sorted_films = doubanspider.sort_films(films_dic)

for film in sorted_films:
    print film[0], ":", film[1]
