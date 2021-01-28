# -*- coding: utf-8 -*-
# @Time : 2020/2/10
# @Author : kiwi
# @File : login_library.py
# @Project : spider
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


def login(usr, pwd):
    url = 'http://www.lib.cdut.edu.cn/'

    options = Options()    # 初始设置参数变量
    options.add_argument('--headless')	 # 不输出图形
    options.add_argument('--no-sandbox')
    # options.binary_location = r'E:\\tmp\\bin\\chrome.exe'
    # driver = webdriver.Chrome(options=options,executable_path="/usr/local/share/chromedriver.exe")
    # driver = webdriver.Chrome("E:\\tmp\\Application\\chrome.exe")
    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome()
    try:
        driver.get(url)
    
        # 输入账户密码
        driver.find_element_by_id('J_Username').send_keys(usr)
        driver.find_element_by_id('J_Password').send_keys(pwd)
        # 登录
    
        driver.find_element_by_class_name('btn').click()
    except:
        print("图书馆账户密码不正确或响应超时 ", time.ctime())
        driver.quit()
        return 0
    # 加载
    time.sleep(0.5)

    return driver

    # driver.switch_to_window(driver.window_handles[0])
    # driver.quit()
    #
    #
    # return res
    # # return get_url


def main():
    usr = '201712090414'
    pwd = '251123'
    print(login(usr, pwd))


if __name__ == '__main__':
    main()
