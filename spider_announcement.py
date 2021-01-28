# -*- coding: utf-8 -*-
# @Time : 2020/1/24
# @Author : kiwi
# @File : spider_calendar.py
# @Project : lydf
import requests
from bs4 import BeautifulSoup
import lxml
import re
import time

def getAnnouncement():
    # < span class ="p_t" > 共18页 < / span >
    url_Announce = 'http://www.aao.cdut.edu.cn/index/jwtz_gg.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/77.0.3865.120 Safari/537.36'
    }
    try:
        resp = requests.get(url_Announce, headers=headers)
        resp.encoding = 'utf-8'
        page = re.findall('<span class="p_t">共(\d*)页</span>', resp.text, re.I)
        # print(page[0])
    except:
        print("教务处公告页面加载失败")
        status = {
            'status': -1,
            'description': '页面不存在或响应超时'}
        return status
    
    announce_sum = []
    for num in range(int(page[0]), 0, -1):
        if num != int(page[0]):
            num = str(num)
            url_Announce = 'http://www.aao.cdut.edu.cn/index/jwtz_gg/' + num + '.htm'
            # print(url_Announce)

        resp = requests.get(url_Announce, headers=headers)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'lxml')
        time.sleep(0.5)

        # http://www.aao.cdut.edu.cn/info/1171/3046.htm
        # announce_sum = []
        for i in soup.find(name='div', attrs={'class': 'content'}).findAll('li'):
            # soup.select('li')[0].get_text().strip()
            #     print(i.span.text)
            #     print('http://www.aao.cdut.edu.cn/' + i.a.get('href'))
            dict_announce = {'title': i.span.text + "(" + i.find('span', class_='hidden-xs hidden-sm').text + ")", 'link': 'http://www.aao.cdut.edu.cn/' + i.a.get('href')}
            announce_sum.append(dict_announce)
        # print(announce_sum)
        # print(announce_sum.__len__())

    announce_sum_dict = {
        'announce': announce_sum,
        'status': 1,
        'description': 'success'
    }
    return announce_sum_dict
    # print(announce_sum)
    # print(announce_sum.__len__())


if __name__ == "__main__":
    print(getAnnouncement())
