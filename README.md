#python爬虫

powered by *py新手,渣前端*


将[豆瓣电影](http://movie.douban.com/)影里正在上映的电影爬下来,并按得分高低顺序排列,可按照
    
    url="http://movie.douban.com/nowplaying/beijing/"
    get_sort_films(url)


进行调用


pyspider包含两个py文件,douban_movie_spider.py和douban_movie_spider2.py，其中douban_movie_spider.py基于py3,而douban_movie_spider2.py基于py2,两者都需要用到beautiful soup 4的库,py3的版本附带了一个图片下载功能


两者返回的形式均为[列表]=[{字典},{字典},{字典}...]


~~在[百度云](http://pyspider2014.duapp.com/)上搭建了一个tornado来显示douban_movie_spider2.py爬下来的*豆瓣北京*的正在上映电影~~
百度云的价格也太高了点吧,穷学生承受不起...


电影天堂用了一串js来反爬虫,所以不得已用正则把js的函数挑出来再用python处理.

##TODO

~~加入dytt8的电影信息~~
