# -*- coding: utf-8 -*-
# @Time : 2020/1/24
# @Author : kiwi
# @File : spider_calendar.py
# @Project : lydf
import requests
from bs4 import BeautifulSoup
import lxml
import re

def getCalendar():
    url = 'http://www.aao.cdut.edu.cn/index/jxrl.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/77.0.3865.120 Safari/537.36'
    }

    # 日历界面
    # <a href="../info/1192/1444.htm"><span>成都理工大学2018-2019学年教学日历</span></a>
    try:
        resp = requests.get(url, headers=headers)
        resp.encoding = 'utf-8'
        result = re.findall('<a href=\"../(.*?)\"><span>成都理工大学', resp.text, re.I)
    except:
        print("校历页面加载失败")
        status = {
            'status': -1,
            'description': '页面不存在或响应超时'}
        return status
    # print("http://www.aao.cdut.edu.cn/" + result[0])
    # return "http://www.aao.cdut.edu.cn/" + result[0]

    # 日历图片
    # http://www.aao.cdut.edu.cn/__local/2/D5/BC/3FA285999774FEE3720881693CB_74F58DDC_51FD5.pdf
    url_concrete = "http://www.aao.cdut.edu.cn/" + result[0]
    resp2 = requests.get(url_concrete, headers=headers)
    resp2.encoding = 'utf-8'
    result_pic = re.findall('src=\"/__local/(.*?).pdf\"', resp2.text, re.I)
    # print("http://www.aao.cdut.edu.cn/__local/"+result_pic[0]+".pdf")
    calender = {
        'link': "http://www.aao.cdut.edu.cn/__local/"+result_pic[0]+".pdf",
        'status': 1,
        'description': 'success'
    }
    return calender


if __name__ == "__main__":
    print(getCalendar())
