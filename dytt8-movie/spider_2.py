#!/usr/bin/python
#coding:utf-8

import urllib2
import bs4
import re
import chardet

class Dytt8Spider:
    def __init__(self):
        self.__headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
        self.__opener = urllib2.build_opener()
        self.__opener.addheaders = [self.__headers]

    # open an URL
    def open_url(self, url):
        content = self.__opener.open(url).read()
        encoding = chardet.detect(content)['encoding']
        content = content.decode(encoding, 'ignore')
        return content
    
    # return all the film tags
    def get_films(self, content):
        soup = bs4.BeautifulSoup(content)
        # list of tags "a" with attribute "class=ulink"
        films_list = soup.findAll('a', class_='ulink')  
        return films_list

    # retrieve the download url in every film tag
    def get_download_url(self, films_list):
        films_list_url = []
        # iterate every tag
        for film in films_list:
            film_dic = {}
            # get url
            film_href = "http://www.dytt8.net" + film['href']
            # open url
            film_content = self.__opener.open(film_href).read()
            encoding = chardet.detect(film_content)['encoding']
            film_content = film_content.decode(encoding, 'ignore')
            # create a BeautifulSoup object
            film_soup = bs4.BeautifulSoup(film_content)
            # get film title
            title_all = film_soup.findAll('div', class_='title_all')
            film_dic['film_title'] = title_all[-1].h1.font.string
            # get download url
            if film_dic['film_title']:
                film_dic['download_url'] = film_soup.findAll('td', style='WORD-WRAP: break-word')[0].a['href']
                films_list_url.append(film_dic)
            else:
                break
        return films_list_url
