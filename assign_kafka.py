# -*- coding: utf-8 -*-
# @Time : 2021/1/29
# @Author : kiwi
# @File : assign_kafka.py
# @Project : spider

from jobsearch import getJobInfo


# 写入文件
def outputFile():
    print('read')
    with open('./jobdata.txt', 'r', encoding='utf-8') as file:
        a = file.readline()
        print(a)



if __name__ == "__main__":
    pass
