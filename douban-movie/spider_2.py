#!/usr/bin/python
#coding: utf-8

import urllib2  # functions and classes which help in opening URLs
import bs4      # extract data from HTML or XML files
import chardet  # detect encoding character of HTML file
import re

class DoubanSpider:
    def __init__(self):
        self.__headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    
    def open_url(self, url):
        opener = urllib2.build_opener()           # create an OpenerDirector object
        opener.addheaders = [self.__headers]      # set HTTP headers
        content = opener.open(url).read()         # open the url and get the corresponding HTML contents
        encoding = chardet.detect(content)['encoding']  # changing character encoding
        content = content.decode(encoding, 'ignore')
        return content

    def get_films(self, content):
        soup = bs4.BeautifulSoup(content)
        div=soup.find('div', id='nowplaying')               # return the first "div" tag
        films_list = div.findAll('li', class_="list-item")  # return the list of "li" tag under "div"
        return films_list

    def sort_films(self, films_list):
        films_sorted = []

        for film in films_list:  
            # For each film
            film_dic = {}
            if (film.ul.li['class'] == ['poster']):  
                # retrieve corresponding informations
                film_dic['film_name'] = film.ul.li.img['alt']
                film_dic['film_release'] = film['data-release']
                film_dic['film_actors'] = film['data-actors']
                film_dic['film_director'] = film['data-director']
                film_dic['film_href'] = film.ul.li.a['href']
                film_dic['film_src'] = film.ul.li.a.img['src']
                # get scores
                if film.find('span', attrs={'class': 'subject-rate'}):
                    # if there is
                    film_dic['film_points'] = film.find('span', {'class','subject-rate'}).string.strip()
                    if str(film_dic['film_release']) == '2014':
                        film_dic['points'] = float(film_dic['film_points'])+10
                    else:
                        film_dic['points'] = float(film_dic['film_points'])
                else:
                    # if there isn't
                    film_dic['film_points'] = u'暂无评分'
                    if str(film_dic['film_release']) == '2014':
                        film_dic['points'] = 10
                    else:
                        film_dic['points'] = 0
                # get stars
                stars = film.find('li', attrs={'class': 'srating'}).span['class']
                if stars[0] != 'rating-star':
                    # if there isn't
                    film_dic['film_stars'] = u'评价人数不足'
                else:
                    # if there is 
                    str_stars=stars[1]
                    match = re.match(r'^(\D+)(\d{2})$', str_stars)
                    film_dic['film_stars'] = str(int(match.group(2)) / 10).decode('utf-8') + u'颗星'
            # add all the informations of a film into list "films_sorted"
            films_sorted.append(film_dic)

        films_sorted = sorted(films_sorted, key=lambda x:x['points'], reverse = True)
        return films_sorted
