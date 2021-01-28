# -*- coding: utf-8 -*-
# @Time : 2020/2/11
# @Author : kiwi
# @File : library_borrow.py
# @Project : spider
from login_library import login
from bs4 import BeautifulSoup


def getBorrowRecord(username, psw):
    driver = login(username, psw)
    if driver == 0:
        status = {
            'status': -1,
            'description': '图书馆账户密码不正确或响应超时'}
        return status
    # 获取url
    driver.find_element_by_class_name('user').click()
    get_url = driver.current_url
    driver.get(get_url)
    res = driver.page_source
    # return res
    soup = BeautifulSoup(res, 'lxml')
    table = soup.find(name='form', attrs={'name': 'form1'}).findAll('table')[0]
    num = 0
    book_records = []
    for trs in table.tbody.findAll('tr'):
        if num < 1:
            num += 1
            continue
        record = []
        for td in trs.findAll('td'):
            # print(td.text)
            record.append(td.text)
        book_record = {
            '借阅图书名': record[0],
            '条形码': record[1],
            '外借时间': record[3],
            '归还时间': record[4]
        }
        book_records.append(book_record)
    records_dict = {
        'book_records': book_records,
        'status': 1,
        'description': 'success'
    }
    # print(book_records)
    return records_dict


if __name__ == "__main__":
    getBorrowRecord()
