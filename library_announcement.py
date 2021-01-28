# -*- coding: utf-8 -*-
# @Time : 2020/2/11
# @Author : kiwi
# @File : library_announcement.py
# @Project : spider
import requests
import re
from bs4 import BeautifulSoup


def getLibAnnounce():
    url_Announce = 'http://www.lib.cdut.edu.cn/category8/index.shtml?pager.offset=0'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/77.0.3865.120 Safari/537.36'
    }
    try:
        resp = requests.get(url_Announce, headers=headers)
        resp.encoding = 'utf-8'
    
        # print(resp.text)
        sum_num = int(re.findall('<a href=\"/category8/index.shtml\?pager.offset=(.*?)\" title="尾页"', resp.text, re.I)[0])
        # print(sum_num)
    except:
        print("图书馆公告页面加载失败")
        status = {
            'status': -1,
            'description': '页面不存在或响应超时'}
        return status

    page_num = 0
    announce_sum = []
    while page_num <= sum_num:
        url_Announce = 'http://www.lib.cdut.edu.cn/category8/index.shtml?pager.offset={}'.format(page_num)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/77.0.3865.120 Safari/537.36'
        }
        resp = requests.get(url_Announce, headers=headers)
        resp.encoding = 'utf-8'

        soup = BeautifulSoup(resp.text, 'lxml')

        for li in soup.find(name='ul', attrs={'class': 'lict_cont1 clearfix'}).findAll('li'):
            announce = {}
            # print(''.join(li.text.split()))
            # print("http://www.lib.cdut.edu.cn/category8"+li.a['href'])
            announce = {
                'title': ''.join(li.text.split()),
                'link': "http://www.lib.cdut.edu.cn/category8"+li.a['href']
            }
            announce_sum.append(announce)
        page_num += 15

    # print(announce_sum)
    announce_sum = {
        'lib_announce': announce_sum,
        'status': 1,
        'description': 'success'
    }
    return announce_sum


if __name__ == "__main__":
    getLibAnnounce()
