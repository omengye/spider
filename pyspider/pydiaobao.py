# -*- coding: utf-8 -*-
import urllib2
import re
import bs4
import time

url = "http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFt44Og04hmxhSXzx9VX68VHg&page=1&t=1410605235579"
urls = []
urls.append(url)    # 以列表形式呈现所有页数的url

class SimpleCookieHandler(urllib2.BaseHandler): # 添加自定义cookie

    def http_request(self, req):
        simple_cookie = 'SUID=8614F37266CA0D0A0000000053A6EB57; SUV=1403448156290881; CXID=D570E9D33EF902902AAEE5245112E2EC; ssuid=6218322088; pgv_pvi=4723382272; sct=5; LSTMV=215%2C288; LCLKINT=6490; SNUID=09B247C6B5B1B66A660F93ECB515CB94; PHPSESSID=h0mvenu4sgela33q7s5145f920; SUIR=09B247C6B5B1B66A660F93ECB515CB94; IPLOC=CN1101; ABTEST=3|1411634745|v1'

        if not req.has_header('Cookie'):
            req.add_unredirected_header('Cookie', simple_cookie)
        else:
            cookie = req.get_header('Cookie')
            req.add_unredirected_header('Cookie', simple_cookie + '; ' + cookie)
        return req

def get_html_content(url=None):
    headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(), SimpleCookieHandler())
    opener.add_handler = headers
    return opener.open(url).read().decode('utf-8').encode('utf-8')


def find_page_maxNo(html_content = None):

    line = '\"totalPages\"\:(.+?)\}'
    maxNo = re.findall(line, html_content)[0]   # 查找最大页数

    return int(maxNo)

maxNo = find_page_maxNo(get_html_content(url))

print u'总页数' + str(maxNo)

# 查找并替换url中page的值
def replace_url(url=None, Max=1):
    rule = re.compile('page\=\d\&')
    for i in range(2, Max):
        new_url = re.sub(rule,'page='+str(i)+'&', url)
        urls.append(new_url)
    return urls

urls = replace_url(url, maxNo+1)


def find_key_url(html_content = None):

    line = r'sogou.weixin.gzhcb([\s\S]*)\r\n'
    raw_content = re.findall(line, html_content)[0][1:-1]   # 提取内容部分

    rule1 = re.compile(r'\xee\x91\xa8') # 删除内容里的未知编码
    raw1 = re.sub(rule1,'',raw_content)

    raw1_dict = eval(raw1)  # 转变unicode str到dict

    key_url = []

    for item in raw1_dict['items']:
        compile2 = re.compile('\\\\')   # 将单个反斜杠 \ 匹配删除
        raw2 = re.sub(compile2,'',item)

        search_key = re.compile('\<title\>\<\!\[CDATA\[(.+?)\:')    # 匹配出title的值
        key = search_key.search(raw2)
        if key.group(1) == u'美女醒床图'.encode('utf-8'):
            j = re.compile('\<\/title\>\<url\>\<\!\[CDATA\[(.+?)\]')    # 找出符合title条件的url
            find_url = j.findall(raw2)
            key_url.append(find_url[0])

    return key_url


key_urls = []   # 循环查找所有页选出符合条件的url
for page_url in urls:
    content = get_html_content(page_url)
    key_url = find_key_url(content)
    key_urls.extend(key_url)

print u'Items Num:' + str(len(key_urls))


def get_pic_url(url=None):  # 挑出页面中所有的图片链接
    page_content = get_html_content(url)
    soup = bs4.BeautifulSoup(page_content)
    pic_url = []
    i = soup.find('div',{'class':'rich_media_thumb'})
    pic_url.append(i.img['src'])

    j = soup.findAll('p')
    for it in j:
        if it.img:
            if it.img.has_attr('data-src'): # 判断tag是否含有 'data-src' 属性值
                pic_url.append(it.img['data-src'])
            elif it.img.has_attr('src'):
                pic_url.append(it.img['src'])

    return pic_url


all_pic_urls = []
j = 0
for i in key_urls:
    j = j + 1
    print 'page url:' + str(j) + '\n'

    all_pic_urls.extend(get_pic_url(i))
    time.sleep(5)   # 间隔5秒采集一次

print u'查找结束'

final_urls = filter(lambda x : all_pic_urls.count(x) == 1, all_pic_urls) # 删除所有重复项

ads_url = [u'http://mmbiz.qpic.cn/mmbiz/ibfSwYkJfj0szae7EVSRVB17MttuDmyeAiaDGIYB3nSsdqFEqqTBOUXLUljbTylbcwBHybrKlg3d1gIKL1TCecKw/0', u'http://mmbiz.qpic.cn/mmbiz/ibfSwYkJfj0uOajPmwUAfTcOKGgMgZ8WWicObJxCfRrDffFZ5ntsHvLVW7wD0nQmndXVbGCIjkVqEFNZmbNCFOnQ/0', u'http://mmbiz.qpic.cn/mmbiz/ibfSwYkJfj0vhRQTTKMfXFewrcBNmSkCNlKK0Z1cgG5vsE1hWahv7FcPLtQKohl7P8FsAib6egwYLalhVDMfKclQ/0', u'http://mmbiz.qpic.cn/mmbiz/ibfSwYkJfj0uAZrg1531grGPKBMTxGl10iceKiaYuaUacLpyur6rjCSia1VHGGgBnMWmP9ZkWSGWBKfsoa2YAicv27A/0', u'http://mmbiz.qpic.cn/mmbiz/ibfSwYkJfj0vrmzIlOraTIBCMoj9gTPgERXdgiaOKYibA5NicgqwACHNZ2ZPWE8rxrNOQVqtpLQLvfzX6pNNbut2bg/0', u'http://mmbiz.qpic.cn/mmbiz/ibfSwYkJfj0uThUx5P4hF3SD4mHfuEYENUib0yclhrrTxygnOebNI8T71q7sqHsgNZjc8ENJQGiaAqxX3GA6C8mWg/0', u'http://mmbiz.qpic.cn/mmbiz/ibfSwYkJfj0sMtKicPnL9DcJDaGXz1r0CbyOuSLgm53iaC3DQibKibjIddP1L4JoAD5hibRTKMApbKCuEa9oMFNyQPEw/0', u'http://mmbiz.qpic.cn/mmbiz/ibfSwYkJfj0vVCr7JCPxTkoPwjx5XFRfoQGjLrG3Ra0iaiawH8kY0T8SBhpnLTAmibMyVJ6kuxWycrzlOzibPib8Zewg/0', u'http://mmbiz.qpic.cn/mmbiz/ibfSwYkJfj0vawYnPZgcqJHBArOz9fgFDJDuo7RLIkeyzPRSYo9eQKVk1tTGN9ibHtdkbpVFicMV6jhgmj4UjJZhA/0', u'http://mmbiz.qpic.cn/mmbiz/ibfSwYkJfj0sDIdtelVgrTkpCbHXEChpT6CcdzIXFibrjcqnBGUH9kRPRR5FGKPD0O8xibGfrfPJsSbVfic0wh6F6w/0', u'http://mmbiz.qpic.cn/mmbiz/ibfSwYkJfj0vvbiaqjd2NUjRBBPIHfvfFdXbvvebF6iciaoCPQt0k0kKp4QjVEssU5kHlUEtibQosTQ0V0oNx76o3Tw/0', u'http://mmbiz.qpic.cn/mmbiz/ibfSwYkJfj0se9zDkaAfBNpHlhWU1AwD3eiaBZiaiblloW1VkKWyTgg8Gq3dX8GusqZoX2XgYekicn1oPwxm7foVdeA/0']


for ad_url in ads_url:
    if ad_url in final_urls:
        del_ad = final_urls.index(ad_url)
        del final_urls[del_ad]  # 删除广告图片

print final_urls
