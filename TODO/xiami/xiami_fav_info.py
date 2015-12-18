import http.cookiejar
import urllib.request
import bs4
import math
import string
import time


def is_all_num(str_num):
    # 判断字符串是否全为数字
    for i in str_num:
        if i not in string.digits:
            return False

    return True


def get_html_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,*/*',
        'Cache-Control': 'no-cache',
        'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
        'DNT': '1'
    }

    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read()

    html_soup = bs4.BeautifulSoup(content)

    return html_soup


def get_music_num(url):
    soup_html = get_html_soup(url)

    counts = soup_html.find('span', {'class': 'counts'}).string[0:-1]

    return counts


def get_page_num(url):
    music_num = int(get_music_num(url))

    if music_num == 0:
        return 1
    elif music_num % 25 == 0:
        return math.floor(music_num / 25)  # 每页25行
    else:
        return math.floor(music_num / 25) + 1


def get_page_songs_info(url):
    soup_html = get_html_soup(url)

    songs = soup_html.findAll('td', {'class': 'song_name'})

    songs_info = []
    for song in songs:
        info = song.findAll('a')

        title_id = info[0].get('href').split("/")[-1]
        title = info[0].string

        artist_id = info[1].get('href').split("/")[-1]
        if is_all_num(artist_id) is False:
            artist_id = ""

        artist = info[1].string

        song_info = {'title_id': title_id, 'title': title, 'artist_id': artist_id, 'artist': artist}

        songs_info.append(song_info)

    return songs_info


def get_all_page(url):
    pages = []
    common_url = url[0:-1]

    page_num = get_page_num(url)
    for i in range(page_num):
        pages.append(common_url + str(1 + i))

    return pages


def get_all_music(url):
    page_songs = get_page_songs_info(url)
    all_music_info.extend(page_songs)


URL = "http://www.xiami.com/space/lib-song/u/2339876/page/1"

all_music_info = []

count = 1
for page_url in get_all_page(URL):
    get_all_music(page_url)
    time.sleep(5)
    print(count)
    count += 1

print(all_music_info)
