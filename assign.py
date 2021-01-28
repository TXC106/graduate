# -*- coding: utf-8 -*-
# @Time : 2020/6/29
# @Author : kiwi
# @File : assign.py
# @Project : Spider
from bs4 import BeautifulSoup


def spider_deal():
	file = open('test.txt',encoding='utf-8')
	resp = file.read()
	soup = BeautifulSoup(resp, 'lxml')
	# print(soup)
	list_s = []
	for li in soup.findAll(name='div', attrs={'class': 'fl clearfix', 'i': 'font20'}):
		print(li)
		# list_s.append(li.text)
		# for div in li.findAll(_class='fl clearfix'):
		# # print(li.text.replace('',))
		# for div in li.findAll('div'):
		# 	print(div)
	print(list_s)
	# print(len(list(set(list_s))))


if __name__ == "__main__":
    spider_deal()
