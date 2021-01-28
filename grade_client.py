# -*- coding: utf-8 -*-
# @Time : 2020/1/26
# @Author : kiwi
# @File : grade_client.py
# @Project : lydf
from xmlrpc.client import ServerProxy


if __name__ == "__main__":
    server = ServerProxy("http://localhost:8080")
    print(server.test(1, 2))
