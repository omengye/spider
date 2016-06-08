#!/usr/bin/python
#coding:utf-8

import urllib2
import bs4
import chardet

class SpiderDytt8:
    def __init__(self):
        self.__headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64)')
        self.__opener = urllib2.build_opener()
        self.__opener.addheaders = [self.__headers]

    def openUrl(self, url):
        """
        Open a url and return the HTML content
        :param url:
        :return:
        """
        content = self.__opener.open(url).read()
        encoding = chardet.detect(content)['encoding']
        content = content.decode(encoding, 'ignore')
        return content
    
    def getFilms(self, content):
        """
        :param content:
        :return:  a list of all the film tags
        """
        soup = bs4.BeautifulSoup(content, "html.parser")
        # list of tags "a" with attribute "class=ulink"
        filmsList = soup.findAll('a', class_='ulink')
        return filmsList

    def getDownloadUrl(self, films_list):
        """
        get each film with associated download URL
        :param films_list:
        :return:
        """
        filmsUrlList = []
        # iterate every tag
        for film in films_list:
            UrlDic = {}
            # get url
            filmHref = "http://www.dytt8.net" + film['href']
            # open url
            filmContent = self.__opener.open(filmHref).read()
            encoding = chardet.detect(filmContent)['encoding']
            filmContent = filmContent.decode(encoding, 'ignore')
            # create a BeautifulSoup object
            filmSoup = bs4.BeautifulSoup(filmContent, "html.parser")
            # get film title
            titleAll = filmSoup.findAll('div', class_='title_all')
            UrlDic['film_title'] = titleAll[-1].h1.font.string
            # get download url
            if UrlDic['film_title']:
                UrlDic['download_url'] = filmSoup.findAll('td', style='WORD-WRAP: break-word')[0].a['href']
                filmsUrlList.append(UrlDic)
            else:
                break
        return filmsUrlList
