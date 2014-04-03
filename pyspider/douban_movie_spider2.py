# -*- coding: utf-8 -*- 
import urllib2
import re
import bs4

headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')

def get_sort_films(url):
    opener = urllib2.build_opener()
    opener.add_handler = headers
    content = opener.open(url).read().decode('utf-8')
    soup = bs4.BeautifulSoup(content)

    now_playing_film=soup.find('div' , {"id" : "nowplaying"})   # 获取正在上映电影

    list_content = now_playing_film.findAll('li', { "class" : "list-item" })    # 获取电影列表

    all_film_content = []

    for list_film in list_content:
        film_content = {}
        if (list_film.ul.li['class'] == ['poster']):
            film_content['film_name'] = list_film.ul.li.img['alt']
            film_content['film_release'] = list_film['data-release']
            film_content['film_actors'] = list_film['data-actors']
            film_content['film_director'] = list_film['data-director']
            film_content['film_href'] = list_film.ul.li.a['href']
            film_content['film_src'] = list_film.ul.li.a.img['src']
            if list_film.find('span', {'class','subject-rate'}):
                film_content['film_points'] = list_film.find('span', {'class','subject-rate'}).string.strip()
                if str(film_content['film_release']) == '2014':
                    film_content['points'] = float(film_content['film_points'])+10
                else:
                    film_content['points'] = float(film_content['film_points'])
            else:
                if str(film_content['film_release']) == '2014':
                    film_content['points'] = 10
                else:
                    film_content['points'] = 0
                film_content['film_points'] = u'暂无评分'

            stars = list_film.find('li', {'class' :'srating'}).span['class']

            if stars[0] != 'rating-star':
                film_content['film_stars'] = u'评价人数不足'
            else:
                original_film_stars=stars[1]
                re_film_stars=re.compile(r'^\D*(\d{2})$')    # 用正则提取星数
                film_content['film_stars'] = str(int(re_film_stars.search(original_film_stars).groups()[0])/10)+'颗星'

        all_film_content.append(film_content)
    sort_all_film = sorted(all_film_content, key=lambda x:x['points'], reverse = True)    # 将列表中字典元素按从大到小排列

    return sort_all_film
