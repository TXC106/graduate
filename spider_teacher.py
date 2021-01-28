# -*- coding: utf-8 -*-
# @Time : 2020/2/9
# @Author : kiwi
# @File : spider_teacher.py
# @Project : spider
from login import spider_deal
import time
from selenium.webdriver.common.action_chains import ActionChains
from spider_schedule import get_schedule


def getTeacherInfo(username, psw, t_name):
    try:
        driver = spider_deal(username, psw)
    # print(driver.find_element_by_xpath('//*[@id="form1"]/ div[4]/div[1]/ul/li[2]/ul/li[1]/a'))
    # exit()

        # li = driver.find_element_by_xpath('//*[@id="form1"]/div[4]/div[1]/ul/li[2]')
        # li = driver.find_element_by_link_text(u'信息查询')
        li = driver.find_element_by_class_name('nav_menu_03')
        ActionChains(driver).move_to_element(li).perform()
        time.sleep(2)
        # ActionChains.move_to_element(li).send_keys(Keys.DOWN).click().perform()
        # li.find_element_by_xpath('//*[2]/li[1]/a').click()

        driver.find_element_by_xpath('//span[contains(text(),"教师查询")]').click()
        # driver.find_elements_by_class_name('nav_menu_01').click()
        # driver.find_elements_by_partical_link_text("课表查询").click()
        # driver.find_element_by_link_text(u'课表查询').click()
        # driver.find_element_by_xpath('//*[@id="form1"]/div[4]/div[1]/ul/li[2]/ul/li[1]/a').click()
        # driver.find_element_by_xpath('//*[@id="form1"]/ div[4]/div[1]/ul/li[2]/ul/li[1]/a[contains(text(),
        # 课表查询)]').click() driver.find_element_by_link_text(u'课表查询').click() exit() ActionChains(
        # driver).move_to_element(li1).perform() time.sleep(1000) ul = driver.find_element_by_css_selector("div#nav >
        #  ul") ul.find_element_by_id("li2_input_2").click()
        # exit()
    except:
        # print("账户密码不正确或响应超时 ", time.ctime())
        driver.quit()
        status = {
            'status': -1,
            'description': '账户密码不正确或响应超时'}
        return status

    # 输入
    driver.find_element_by_id('Content_txtSearch').send_keys(t_name)
    try:
        driver.find_element_by_class_name('blue_button').click()
    except:
        print("老师名称错误或超时", time.ctime())
        driver.quit()
        status = {
            'status': -1,
            'description': '老师名称错误或超时'}
        return status

    # 详情
    driver.find_element_by_link_text(t_name).click()
    driver.find_element_by_id('Content_Button1').click()
    driver.switch_to_window(driver.window_handles[1])  #

    # 获取新url
    get_url = driver.current_url
    driver.get(get_url)

    res = driver.page_source  # 源码
    schedule = get_schedule(res)

    driver.switch_to_window(driver.window_handles[0])
    driver.quit()

    return schedule


if __name__ == "__main__":
    print(getTeacherInfo('201712090414', '420502199704251123', '刘恒'))
