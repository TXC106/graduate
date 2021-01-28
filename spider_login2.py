# -*- coding: utf-8 -*-
# @Time : 2020/1/24
# @Author : kiwi
# @File : spider_login2.py
# @Project : lydf
import requests
from xmlrpc.server import SimpleXMLRPCServer
from bs4 import BeautifulSoup
import lxml
import time
import datetime
import hashlib
import execjs
# from spider_score import getScore


def hex_md5(data):
    return execjs.compile(open(r'{}/md5.js'.format('/root')).read()).call('hex_md5', data)


def login(username, pwd):

    url_login = 'http://202.115.133.173:805/Common/Handler/UserLogin.ashx'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.87 Safari/537.36',
        # 'Referer': 'http://202.115.133.173:805/Login.html',
        "Origin": "http://202.115.133.173:805",
        "Referer": "http://202.115.133.173:805/Default.aspx",
        "X-Requested-With": "XMLHttpRequest",
        "Upgrade-Insecure-Requests": "1",
    }

    # Action: Login
    # userName:
    # pwd: b6adf8d2fcf32fc0c2a4adc1a3b087e5
    # sign: 1580293526357
    loginForm = {
        'userName': '',
        'pwd': '',
        'sign': '',
        'Action': 'Login'
    }

    # get psw
    sign = str(round(time.time()*1000))
    username = username
    psw = hex_md5(username + sign + hex_md5(pwd.strip()))
    loginForm['sign'] = sign
    loginForm['userName'] = username
    loginForm['pwd'] = psw
    # print(username)
    # print(sign)
    # print(psw)

    try:
        s = requests.Session()
        login1 = s.post(url_login, data=loginForm, headers=headers)
        if login1.text == "0":
            return s
        else:
            return 0
    except:
        return 0


if __name__ == "__main__":
    # server = SimpleXMLRPCServer(("localhost", 8080))
    # server.register_function(test)
    # server.serve_forever()

    login()
    # mstime1 = getTime()
    # mstime2 = getjsTime(datetime.datetime.utcnow())
    # print(mstime2)

