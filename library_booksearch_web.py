# -*- coding: utf-8 -*-
# @Time : 2020/2/11
# @Author : kiwi
# @File : library_booksearch.py
# @Project : spider
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

def searchBooks(bookname):
    url_main = 'http://www.lib.cdut.edu.cn/opac/search?tag=search&q={}'.format(bookname)

    mainPage = searchPages(url_main)
    mainFunc(mainPage)


def searchPages(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/77.0.3865.120 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'

    soup = BeautifulSoup(resp.text, 'lxml')
    div = str(soup.find('div', class_='jp-mainCenter'))

    # # 更换链接
    head_line = 'http://www.lib.cdut.edu.cn/'
    html_search = re.sub(r'(?<=src=\").', head_line, div)

    # 去除多余信息
    delete_info = r'(<strong>出版信息：</strong>.*?</p>)(?:[\s\S]*?)(</li>)'
    new_html_search = re.sub(delete_info, r'\1\2', html_search)
    # new_html_search = re.sub(delete_info, r'\1\2', div)

    # 去除输入框
    html_text = re.sub(r'<input.*?/>', '', new_html_search)

    # 去除空白行 否则写入文件错误
    html_text_nos = re.sub('\s', ' ', html_text)

    return getCompleteHtml(html_text_nos)


def searchBookPages(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/77.0.3865.120 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'

    soup = BeautifulSoup(resp.text, 'lxml')
    table = str(soup.find('table', id='detailsTable'))
    # print(table)
    # location_table = str(soup.find('table', id='gctable'))
    # print(soup.find('table', id='gctable'))

    # return getCompleteDetailHtml(table + location_table)
    return getCompleteDetailHtml(table)



def getCompleteHtml(res):
    headHtml = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
    </head>
    <body>
    <input id="search" type="text"/>
    <button id="search_btn" type="submit" onclick="window.location.href='/opac/search?&q='+document.getElementById('search').value">搜索</button>'''

    endHtml = '''</body>
    </html>'''

    return headHtml+res+endHtml


def getCompleteDetailHtml(res):
    headHtml = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
    </head>
    <body>'''

    endHtml = '''</body>
    </html>'''

    return headHtml+res+endHtml


from socket import *
import re

global mainHtmlText


def handle_client(server_socket, client_socket, mainHtml):
    # 接收对方发送的数据
    recv_data = client_socket.recv(1024).decode("utf-8")  # 1024表示本次接收的最大字节数
    # 打印从客户端发送过来的数据内容
    # print("client_recv:",recv_data)
    request_header_lines = recv_data.splitlines()
    # print(request_header_lines)
    if(request_header_lines == []):
        server_socket.close()
        searchBooks('软件工程')
    # for line in request_header_lines:
    #     print(line)
    # while request_header_lines == []:
    #     time.sleep(1)

    # 返回浏览器数据
    # 设置返回的头信息 header
    response_headers = "HTTP/1.1 200 OK\r\n"  # 200 表示找到这个资源
    response_headers += "\r\n"  # 空一行与body隔开

    # 跳转链接获取
    mainPage = re.match('[^/]+(/[^ ]*)', request_header_lines[0])
    # print(mainPage.group(1) == '/')
    searchPage = re.match('[^/]+(/opac/search[^ ]*)', request_header_lines[0])
    iconPage = re.match('[^/]+(/[^.ico]*)', request_header_lines[0])
    newPage = re.match('[^/]+(/opac/book[^ ]*)', request_header_lines[0])
    head_line = 'http://www.lib.cdut.edu.cn'

    if(mainPage.group(1) == '/'):
        response_body = mainHtml
    if(searchPage != None or iconPage != None):
        if(searchPage != None):
            mainHtml = searchPages(head_line + searchPage.group(1))
            response_body = mainHtml
        else:
            response_body = mainHtml
    if(newPage != None):
        newHtml = searchBookPages(head_line + newPage.group(1))
        response_body = newHtml

    # 返回数据给浏览器
    client_socket.send(response_headers.encode("utf-8"))  # 转码utf-8并send数据到浏览器
    client_socket.send(response_body.encode("utf-8"))
    client_socket.close()


# server_socket = []
import datetime

def mainFunc(mainHtml):
    # print(server_socket)
    # if(server_socket):
    #     server_socket.close()
    # global server_socket
    # 创建套接字
    server_socket = socket(AF_INET, SOCK_STREAM)
    # 设置当服务器先close 即服务器端4次挥手之后资源能够立即释放，这样就保证了，下次运行程序时 可以立即绑定7788端口
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # 设置服务端提供服务的端口号
    server_socket.bind(('', 7788))    # 绑内网会有冲突错误 172.17.218.93
    # 使用socket创建的套接字默认的属性是主动的，使用listen将其改为被动，用来监听连接
    server_socket.listen(128)  # 最多可以监听128个连接
    # 开启while循环处理访问过来的请求
    while True:
        # 如果有新的客户端来链接服务端，那么就产生一个新的套接字专门为这个客户端服务
        # client_socket用来为这个客户端服务
        # server_socket就可以省下来专门等待其他新的客户端连接while True:
        client_socket, clientAddr = server_socket.accept()
        handle_client(server_socket, client_socket, mainHtml)
        if datetime.datetime.now().hour == 21 & datetime.datetime.now().minute == 00:
            client_socket.close()
            break


if __name__ == "__main__":
    searchBooks('软件工程')
