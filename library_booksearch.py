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
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    #                   ' Chrome/77.0.3865.120 Safari/537.36'
    # }
    # resp = requests.get(url_main, headers=headers)
    # resp.encoding = 'utf-8'
    #
    # page_url =
    return url_main



if __name__ == "__main__":
    print(searchBooks('软件工程'))
