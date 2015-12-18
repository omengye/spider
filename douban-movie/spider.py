#!/usr/bin/python
#coding: utf-8

import urllib2  # functions and classes which help in opening URLs
import bs4      # extract data from HTML or XML files
import chardet  # detect encoding character of HTML file
import re

class DoubanSpider:

    # self指向构造函数创建的对象
    def __init__(self):
        # __headers为对象变量,构造对象时创建
        self.__headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    
    # self相当与this指针,指向调用此函数的对象
    def open_url(self, url):
        opener = urllib2.build_opener()           # create an OpenerDirector object
        opener.addheaders = [self.__headers]      # set HTTP headers
        content = opener.open(url).read()         # open the url and get the corresponding HTML contents
        encoding = chardet.detect(content)['encoding']  # changing character encoding
        content = content.decode(encoding, 'ignore')
        return content

    def get_films(self, content):
        films_dic = {}
        soup = bs4.BeautifulSoup(content)
        div=soup.find('div', class_='screening-bd')               # return the first "div" tag
        films_list = div.findAll('li', class_="ui-slide-item")    # return the list of "li" tag under "div"

        for film in films_list:
            if('data-rate' in film.attrs):
                if film['data-rate']:
                    films_dic[film['data-title']] = float(film['data-rate'])

        return films_dic

    def sort_films(self, films_dic):
        sorted_films = sorted(films_dic.iteritems(), key = lambda x:x[1], reverse = True)
        return sorted_films
