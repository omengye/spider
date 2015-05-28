#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2  # functions and classes which help in opening URLs
import bs4      # extract data from HTML or XML files
import re
import chardet

def get_films_sorted(url):
    headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    opener = urllib2.build_opener()  # create an OpenerDirector object
    opener.addheaders = [headers]    # set HTTP headers
    content = opener.open(url).read()  # open the url and get the corresponding HTML contents
    encoding = chardet.detect(content)['encoding']
    content = content.decode(encoding, 'ignore')


    soup = bs4.BeautifulSoup(content)
    div_now_playing=soup.find('div', id='nowplaying')   # 返回第一个指定属性的div标签
    list_li_films = div_now_playing.findAll('li', class_="list-item")    # 返回一个包含所有li标签,class属性为"list-item"的列表

    films_list = []

    # 遍历每个电影
    for li_film in list_li_films:

        # 字典
        film_dic = {}

        if (li_film.ul.li['class'] == ['poster']):
            # 提取相应信息
            film_dic['film_name'] = li_film.ul.li.img['alt']
            film_dic['film_release'] = li_film['data-release']
            film_dic['film_actors'] = li_film['data-actors']
            film_dic['film_director'] = li_film['data-director']
            film_dic['film_href'] = li_film.ul.li.a['href']
            film_dic['film_src'] = li_film.ul.li.a.img['src']

            # 属性也可以用字典定义
            if li_film.find('span', attrs={'class': 'subject-rate'}):
                # 如果有评分
                film_dic['film_points'] = li_film.find('span', {'class','subject-rate'}).string.strip()
                if str(film_dic['film_release']) == '2014':
                    film_dic['points'] = float(film_dic['film_points'])+10
                else:
                    film_dic['points'] = float(film_dic['film_points'])
            else:
                # 如果没评分
                film_dic['film_points'] = u'暂无评分'
                if str(film_dic['film_release']) == '2014':
                    film_dic['points'] = 10
                else:
                    film_dic['points'] = 0

            # stars为class属性的内容
            stars = li_film.find('li', attrs={'class': 'srating'}).span['class']

            if stars[0] != 'rating-star':
                # 没有评星
                film_dic['film_stars'] = u'评价人数不足'
            else:
                # 有评星
                str_stars=stars[1]
                match = re.match(r'^(\D+)(\d{2})$', str_stars)
                film_dic['film_stars'] = str(int(match.group(2)) / 10).decode('utf-8') + u'颗星'

        films_list.append(film_dic)

    films_list_sorted = sorted(films_list, key=lambda x:x['points'], reverse = True)

    return films_list_sorted
