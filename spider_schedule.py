# -*- coding: utf-8 -*-
# @Time : 2020/2/7
# @Author : kiwi
# @File : spider_schedule.py
# @Project : spider
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from login import spider_deal
from bs4 import BeautifulSoup
import requests
import lxml
import json
import re


def getColspan(num):
    if num == None:
        return 1
    else:
        return num


def getstartTime(num):
    start_time = {
        1: '8:10',
        3: '10:15',
        6: '14:30',
        8: '16:05',
        10: '19:10'
    }
    return start_time.get(num % 12)


def getendTime(num):
    end_time = {
        2: '9:45',
        4: '11:50',
        7: '16:05',
        9: '18:00',
        11: '20:45',
        0: '21:35'  # 12
    }
    return end_time.get(num % 12)


def getInfo(table):
    course_sum_dict = {}
    for tr in table.tbody.findAll('tr'):
        for td in tr.findAll('td'):  # course
            td_text = td.text
            if td_text != '':
                # info = re.findall('\(\[(.*?)\]\)', td_text)
                infos = re.findall('\((.*?)\)', td_text)
                # course = re.findall('\)(.*?)\(', td_text)[0]
                course_check = re.findall('\)(.*?)\(', td_text)  # 老师课表详情可能无缩写
                if course_check != []:
                    course = course_check[0]

            # place = str(re.findall('室\[(.*?)\]', td_text))  # place
            # print(type(td_text))
            # if info != '':
            #     # info = "([" + info + "])"
            #     for i in info:
                info_len = infos.__len__()
                type_dict = {}
                for i in range(0, info_len):  # type
                    # print(course)
                    # i = "(" + i + ")"
                    info = infos[i]
                    # print(i)
                    # print(info)

                    if i == 0:
                        abbr = info  # 缩写
                        course_dict = {abbr: {}}
                        continue

                    course_type = re.findall('\[(.*?)\]', info)[0]
                    teacher = re.findall('师\[(.*?)\]', info)[0]
                    # 老师课表可能有多个教室
                    places = re.findall('室\[(.*?)\]', info)[0]
                    places = re.split('[,-]', places)
                    for place in places:
                        # print(course_type)

                        # print(teacher)
                        # print(place)
                        type_dict = {
                            place: {
                                'course': course,
                                'type': course_type,
                                'teacher': teacher,
                                'place': place
                            }
                        }
                        course_dict[abbr].update(type_dict)
                        # print(course_dict[abbr])
                        # print(course_dict)
                        # print(type_dict)
                        # course_sum_dict.update(type_dict)
                # print(type(td.getText()))
                # print(td.getText())  # 引号有问题
                # print(td.text)
                # print(info)
                # print(course)
                # print(place)
            # print(course_dict)
            course_sum_dict.update(course_dict)
    print(course_sum_dict)
    # exit()
    return course_sum_dict


def get_schedule(res):
    # 得表
    soup = BeautifulSoup(res, 'lxml')
    tables = soup.findAll('table')
    # print(tables[1])
    table = tables[1]

    # 得具体信息
    table_info = tables[2]
    course_sum_dict = getInfo(table_info)
    # return getInfo(table_info)
    # exit()


    # for tr in table.tbody.findAll('tr'):
    course_table = []
    for tr_num in range(2, 21):  # week
        # tr_num = 6
        tr = table.tbody.findAll('tr')[tr_num]
        coursetime = tr.find('td', class_='td1').text[3:8]
        coursetime_end = int(tr.find('td', class_='td1').text[-2:])
        # print(coursetime_end)
        # exit()
        # print(ctime)
        # print(ctime.split('/'))
        # print(coursetime)
        # continue
        month = int(coursetime.split('/')[0])
        date = int(coursetime.split('/')[1])
        # num = 0
        # for td in tr.findAll('td'):
        tds = tr.findAll('td')
        start = 0
        day = 0
        week = tr_num - 1
        day_list = []
        day_dict = {}
        day_time_list = ['Mon.', 'Tue.', 'Wed.', 'Thur.', 'Fri.', 'Sat.', 'Sun.']
        week_dict = {"week_num": week}
        tdate = date
        for td in tds:  # day
            # day_time = day_time_list[day]
            end = start + int(getColspan(td.get('colspan')))  # 下一节开始
            # print(end)
            if td.get('align') == 'center':
                # print(end - 1)
                # print(getendTime(end - 1))
                # print(start)
                # print(getstartTime(start))
                # print(td.getText())
                # print(getendTime(end))

                # print(getstartTime(start) + ' ' + td.getText() + ' ' + getendTime(end - 1))

                # print(str(start) + ' ' + td.getText() + ' ' + str(end))
                # print(td.getText())
                # print(td.find(name='font', attrs={'class': 'roomcss'}).text)

                # class_room = str(td.find(name='font', attrs={'class': 'roomcss'}).text)
                class_room = td.find(name='font', attrs={'class': 'roomcss'})
                course = td.getText()
                if class_room != None:
                    class_room = class_room.text
                    course = course.replace(class_room, '')
                    course_abbr = course[0: -2]
                    # course = td.getText().replace(class_room, '')
                    if class_room not in course_sum_dict[course_abbr]:  # 老师课表有的详情不全
                        type = ''
                        course = course_abbr
                        teacher = ''
                    else:
                        type = course_sum_dict[course_abbr][class_room]['type']
                        course = course_sum_dict[course_abbr][class_room]['course'] + "[" + type + "]"
                        teacher = course_sum_dict[course_abbr][class_room]['teacher']
                else:
                    class_room = ''
                    teacher = ''
                    # course = td.getText()
                course_dict = {
                    "month_time": month,
                    "date_time": tdate,
                    "begin": getstartTime(start),
                    "end": getendTime(end - 1),
                    "course": course,
                    "teacher": teacher,
                    "class_room": class_room
                }
                # print(class_room)
                day_list.append(course_dict)
            start = end
            if (end - 1) % 12 == 0:
                if day_list:
                    day_time = day_time_list[day - 1]
                    day_dict = {day_time: day_list}
                    # print(day_dict)
                    # print(week_dict)
                    # print(type(week_dict))
                    # print(week_dict)
                    week_dict.update(day_dict)
                    # print(week_dict)
                if day != 0:
                    if tdate < 29:
                        tdate += 1
                    else:
                        if day + coursetime_end < 8:
                            tdate += 1
                        else:
                            tdate = 1
                day_list = []
                day += 1
                if day == 8:
                    break

                # print(td.get('colspan'))
                # if td.get('align') == 'center':
                # print(td.getText())

        # print(week_dict)
        # print(day_dict)
        course_table.append(week_dict)
    schedule = {
        'course_table': course_table,
        'status': 1,
        'description': 'success'
    }
    # print(schedule)
    return schedule



    # day = []
    # for num in range(1, 10):
    #     text = tds[num].getText()
    #     place = tds[num].find(name='font', attrs={'class': 'roomcss'})
    #     # place = tds[num].find(name='font', attrs={'class': 'roomcss'}).text
    #     # print(text)
    #     # print(place)
    #     # print(text.replace(str(place), ''))
    #     if text.isspace() is not True:
    #         # print(switch_mon(num)+text)
    #         text = text.replace(str(place.text), '')
    #         course = {}
    #         course = {
    #             'begin': switch_mon(num)[0],
    #             'end': switch_mon(num)[1],
    #             'name': text,
    #             'place': place.text
    #                   }
    #         print(course)
    #         day.append(course)
    # print(day)

        # print(text)
        # text = td.getText()
        # print(text)

    # print(res)
    # return res


def get_personal_schedule(username, psw):
    driver = spider_deal(username, psw)
    try:
        driver.find_element_by_xpath('//*[@id="form1"]/div[4]/div[3]/div[2]/div[2]/ul/li[1]/a').click()
    except:
        print("账户密码不正确或响应超时（课程表） ", time.ctime())
        driver.quit()
        status = {
            'status': -1,
            'description': '账户密码不正确或响应超时'}
        return status
    driver.switch_to_window(driver.window_handles[1])

    # 获取url
    get_url = driver.current_url
    # print(get_url)
    driver.get(get_url)
    res = driver.page_source  # 源码
    # return res
    # print(type(res))

    driver.switch_to_window(driver.window_handles[0])
    driver.quit()

    return get_schedule(res)


if __name__ == "__main__":
    print(get_personal_schedule('201712090414', '420502199704251123'))

