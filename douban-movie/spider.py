#!/usr/bin/python
#coding: utf-8

import urllib2  # library which helps in opening URL
import bs4      # extract data from HTML or XML files
import chardet  # detect character encoding

class DoubanSpider:

    # self指向构造函数创建的对象
    def __init__(self):
        # __headers为对象变量,构造对象时创建
        self.__headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    
    # self相当与this指针,指向调用此函数的对象
    def open_url(self, url):
        opener = urllib2.build_opener()           # create an OpenerDirector object
        opener.addheaders = [self.__headers]      # set HTTP headers
        file_like_obj = opener.open(url)          # open the url and return a file like object
        content_str = file_like_obj.read()        # get HTML content of the opened file like object
        file_like_obj.close()

        # detect character encoding of content
        content_encoding_dic = chardet.detect(content_str)
        content_encoding = content_encoding_dic['encoding']

        # decode content with indicated character encoding
        content_str = content_str.decode(encoding=content_encoding, errors='ignore')
        return content_str

    def get_films(self, content):
        films_dic = {}
        soup = bs4.BeautifulSoup(content)
        div=soup.find('div', class_='screening-bd')               # get the first "div" tag
        films_list = div.findAll('li', class_="ui-slide-item")    # get the list of "li" tag under "div"

        for film in films_list:
            if('data-rate' in film.attrs):
                if film['data-rate']:
                    films_dic[film['data-title']] = float(film['data-rate'])

        return films_dic

    def sort_films(self, films_dic):
        # iterable: 可迭代对象, key: 一个作用于每个元素的函数,用其返回值进行排序
        sorted_films = sorted(films_dic.items(), key = lambda x:x[1], reverse = True)
        return sorted_films
