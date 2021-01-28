# -*- coding: utf-8 -*-
# @Time : 2020/1/24
# @Author : kiwi
# @File : spider_calendar.py
# @Project : lydf
import requests
from bs4 import BeautifulSoup
import json
import lxml
import re


def getMainPic():
    url_main = 'http://www.aao.cdut.edu.cn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/77.0.3865.120 Safari/537.36'
    }
    try:
        resp = requests.get(url_main, headers=headers).text
        soup = BeautifulSoup(resp, 'lxml')
    except:
        print("轮播图页面加载失败")
        status = {
            'status': -1,
            'description': '页面不存在或响应超时'}
        return status

    pic_sum = []
    for i in soup.findAll(name='div', attrs={'class': 'item'}):
        # http://www.aao.cdut.edu.cn/info/1172/2660.htm
        # http://www.aao.cdut.edu.cn//__local/7/92/0A/DA8111CCC135E3FBB86C0F4782F_5847110F_2DCED.jpg
        # print('http://www.aao.cdut.edu.cn/' + i.a.get('href'))
        # print('http://www.aao.cdut.edu.cn/' + i.img.get('src'))
        pic = {'img': 'http://www.aao.cdut.edu.cn/' + i.img.get('src'), 'link': 'http://www.aao.cdut.edu.cn/' + i.a.get('href')}
        pic_sum.append(pic)

    # print(pic_sum)
    # print(pic_sum.__len__())

    pic_sum_dict = {
        'mainpic': pic_sum,
        'status': 1,
        'description': 'success'
    }
    return pic_sum_dict


if __name__ == "__main__":
    pass
