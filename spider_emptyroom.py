# -*- coding: utf-8 -*-
# @Time : 2020/2/10
# @Author : kiwi
# @File : spider_emptyroom.py
# @Project : spider
from login import spider_deal
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup


def getRoomNum(place):
    roomNum = {
        '教学1楼': '01        ',
        '教学2楼': '02        ',
        '教学3楼': '03        ',
        '教学4楼': '04        ',
        '教学5楼': '05        ',
        '六教A座': '06A       ',
        '六教B座': '06B       ',
        '六教C座': '06C       ',
        '教学7楼': '07        ',
        '教学8楼': '08        ',
        '教学9楼': '10        ',
        '东区1教': 'E1        ',
        '东区2教': 'E2        ',
        '环境学院': '2019000001',
        '艺术大楼': 'Y         '
    }
    return roomNum.get(place)


def getDetails(num):
    details = {
        0: '教室名称',
        1: '座位数',
        2: '1-2节',
        3: '3-4节',
        4: '5-6节',
        5: '7-8节',
        6: '9-11节'
    }
    return details.get(num)


def getEmptyRoom(username, psw, place, choose_time):
    try:
        driver = spider_deal(username, psw)

        li = driver.find_element_by_class_name('nav_menu_03')
        ActionChains(driver).move_to_element(li).perform()
        time.sleep(2)

        driver.find_element_by_xpath('//span[contains(text(),"空教室查询")]').click()
    except:
        print("账户密码不正确或响应超时（空教室） ", time.ctime())
        driver.quit()
        status = {
            'status': -1,
            'description': '账户密码不正确或响应超时'}
        return status

    # 选择场所、时间
    temp_place = place
    place = getRoomNum(place)
    try:
        Select(driver.find_element_by_id('Content_dllTeachingBuilding')).select_by_value(place)
        # driver.find_element_by_id('Content_EmptyDate$text').send_keys(choose_time)
        jss = "document.getElementsByName('ctl00$Content$EmptyDate')[0].value='" + choose_time + "'"
        driver.execute_script(jss)
        driver.find_element_by_id('Content_btnSubmit').click()
        time.sleep(3)
    except:
        print("输入格式不正确或响应超时（空教室） ", time.ctime())
        driver.quit()
        status = {
            'status': -1,
            'description': '输入数据格式不正确或响应超时'}
        return status

    res = driver.page_source
    # print(res)
    # exit()

    soup = BeautifulSoup(res, 'lxml')
    rooms = []
    lis = soup.findAll(name='li', attrs={'class': 'item'})
    for li in lis:
        d_num = 0
        room = {}
        for div in li.findAll('div'):
            detail = getDetails(d_num)
            r = {detail: div.text.strip()}
            room.update(r)
            d_num += 1
            # room = {
            #     '教室名称': div[0],
            #     '座位数': div[1],
            #     '1-2节': div[2],
            #     '3-4节': div[3],
            #     '5-6节': div[4],
            #     '7-8节': div[5],
            #     '9-11节': div[6]
            # }
        rooms.append(room)
    rooms = {
        temp_place: rooms,
        'status': 1,
        'description': 'success'
    }

    driver.switch_to_window(driver.window_handles[0])
    driver.quit()

    # print(rooms)
    return rooms


if __name__ == "__main__":
    print(getEmptyRoom('201712090414', '420502199704251123', '教学5楼', '2020-02-09'))
