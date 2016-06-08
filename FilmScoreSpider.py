#!/usr/bin/python
# coding: utf-8

import urllib2  # library which helps in opening URL
import bs4  # extract data from HTML or XML files
import chardet  # detect character encoding


class SpiderDouban:
    # self表示构造函数创建的对象
    def __init__(self):
        # __headers为类变量,对象持有
        self.__headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64)')

    # self指向调用该函数的对象
    def openUrl(self, url):
        """
        打开一个URL,返回其HTML文档内容
        :param url: 要打开的网址
        :return: 字符串形式的HTML文档内容
        """
        opener = urllib2.build_opener()  # create an OpenerDirector object
        opener.addheaders = [self.__headers]  # set HTTP headers
        fileLikeObj = opener.open(url)  # open the url and return a file like object
        contentString = fileLikeObj.read()  # get HTML content of the opened file like object
        fileLikeObj.close()

        # detect character encoding of content
        encodingDictionary = chardet.detect(contentString)
        encoding = encodingDictionary['encoding']

        # decode content with indicated character encoding
        contentString = contentString.decode(encoding=encoding, errors='ignore')
        return contentString

    def getFilmsDictionary(self, content):
        """
        获取所有电影和其相应分数
        :param content: HTML网页文档
        :return: 一个存有电影和其分数的字典
        """
        filmsDictionary = {}
        soup = bs4.BeautifulSoup(content, "html.parser")
        div = soup.find('div', class_='screening-bd')  # get the first "div" tag
        filmsList = div.findAll('li', class_="ui-slide-item")  # get the list of "li" tag under "div"

        for film in filmsList:
            if ('data-rate' in film.attrs):
                if film['data-rate']:
                    filmsDictionary[film['data-title']] = float(film['data-rate'])

        return filmsDictionary

    def sortFilms(self, filmsDictionary):
        """
        将字典按value排序
        :param filmsDictionary: 字典
        :return: 一个字典的键,值元组数组
        """
        sortedFilms = sorted(filmsDictionary.items(), key=lambda x: x[1], reverse=True)
        return sortedFilms
