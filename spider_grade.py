# -*- coding: utf-8 -*-
# @Time : 2020/1/24
# @Author : kiwi
# @File : spider_grade.py
# @Project : lydf
import requests
from xmlrpc.server import SimpleXMLRPCServer
from bs4 import BeautifulSoup
import lxml
import time
import datetime
import hashlib
import execjs
from spider_score import getScore


# def getTime():
#     time_o = int(time.time()*1000)
#     return str(time_o)
#
#
# def getjsTime():
#     # return int(time.mktime(data.timetuple())*1000)
#     time_js = int(time.mktime(datetime.datetime.utcnow().timetuple())*1000)
#     return str(time_js)
#
#
# def getgrade():
#     return 0
#
#
def hex_md5(data):
    # m = hashlib.md5()
    # m.update(data.encode('utf-8'))
    # return m.hexdigest()
    return execjs.compile(open(r'{}\md5.js'.format('E:\owntry\spider')).read()).call('hex_md5', data)


def login(username, pwd):

    url_login = 'http://202.115.133.173:805/Common/Handler/UserLogin.ashx'

    # get sign
    # time_o = getTime()
    # sign = str(time_o)

    # time_js = getjsTime(datetime.datetime.utcnow())
    # sign2 = str(time_js)
    # print(mstime2)

    # get psw
    # hex_md5(user + sign + hex_md5(pwd.trim())

    # psw2 = PyJsHoisted_hex_md5_(username + sign2 + PyJsHoisted_hex_md5_(pwd))
    # print(psw)
    # print(psw2)
    # print(username)
    # # print(sign)
    # print(sign2)
    # userName: 201712090414
    # pwd: 989
    # c5b42d589f34fa3bb234fdd90b8c2
    # sign: 1580919770628
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
    # var sign = new Date().getTime();
    # var user = userName.trim();
    # var signedpwd = hex_md5(user + sign + hex_md5(pwd.trim()));
    # sign = getTime()
    sign = str(round(time.time()*1000))
    username = username
    psw = hex_md5(username + sign + hex_md5(pwd.strip()))
    loginForm['sign'] = sign
    loginForm['userName'] = username
    loginForm['pwd'] = psw
    # print(username)
    # print(sign)
    # print(psw)

    s = requests.Session()
    # r = s.get(url_login, headers=headers)
    # print(r.content)
    # print(r.url)
    # login = s.get(url_login, headers=headers)
    # print(login)
    # print(login.content.decode('utf-8'))
    login1 = s.post(url_login, data=loginForm, headers=headers)
    # print(login1.json())
    # print(login1.url)
    # print(login1)
    # print(login1.text)
    # print(login1.content.decode("utf-8", "ignore"))
    # print(login1.content)
    # print(login1.cookies)

    # get socre
    # 成绩页面
    url_score = 'http://202.115.133.173:805/SearchInfo/Score/ScoreList.aspx'
    # # 下载成绩页面源代码
    # print(s.get(url_score).text)
    res = s.get(url_score).text
    return getScore(res)
    # my_score_url_text = s.get(url_score).text
    # # my_score_soup = BeautifulSoup(my_score_url_text, 'lxml')
    # # score = my_score_soup.find_all()
    # print(my_score_url_text)
    # for i in score:
    #     print(i.div.string)
    # print(my_score_url_text)



if __name__ == "__main__":
    # server = SimpleXMLRPCServer(("localhost", 8080))
    # server.register_function(test)
    # server.serve_forever()

    print(login('201712090414', '420502199704251123'))
    # mstime1 = getTime()
    # mstime2 = getjsTime(datetime.datetime.utcnow())
    # print(mstime2)

