#python爬虫

powered by *py新手,渣前端*

##douban_movie
将[豆瓣电影](http://movie.douban.com/nowplaying/beijing/)中某地区正在上映的电影爬下来,并按得分高低顺序排列,执行:
    
    在main_2.py中设置url(ex. url="http://movie.douban.com/nowplaying/beijing/")
    ./main_2.py

main_2.py与spider_2.py基于Python 2.x, spider_3.py基于Python 3.x(待更新)
所用到的库:urllib2, bs4, chardet. 没有请自行下载

##dytt8_movie
将[电影天堂](http://www.dytt8.net/html/gndy/dyzz/index.html)上的最新电影及其下载地址爬下来,执行:

    在main_2.py中设置url(ex. url="http://www.dytt8.net/html/gndy/dyzz/index.html")
    ./main_2.py

main_2.py与spider_2.py基于Python 2.x, spider_3.py基于Python 3.x(待更新)
所用到的库:urllib2, bs4, chardet. 没有请自行下载

两者返回的形式均为[列表]=[{字典},{字典},{字典}...]

##Remark
~~在[百度云](http://pyspider2014.duapp.com/)上搭建了一个tornado来显示douban_movie_spider2.py爬下来的*豆瓣北京*的正在上映电影~~
百度云的价格也太高了点吧,穷学生承受不起...

电影天堂用了一串js来反爬虫,所以不得已用正则把js的函数挑出来再用python处理.

微信公众号能在搜狗上搜索了,所以爬下来也就不是一个难事了,这里抓取的是公众号碉堡的图片链接.
处理好的demo放在[coding](http://omengye.coding.io/)上了.

##TODO
~~加入dytt8的电影信息~~
Python 3.x下的douban_movie与dytt8_movie
