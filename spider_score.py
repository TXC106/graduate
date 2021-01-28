# -*- coding: utf-8 -*-
# @Time : 2020/2/9
# @Author : kiwi
# @File : spider_score.py
# @Project : spider
from login import spider_deal
import time
from bs4 import BeautifulSoup
import lxml
from spider_login2 import login


def getDetail(num):
    info_switch = {
        0: 'term',
        2: 'Course',
        4: 'Credit',
        5: 'Score'
    }
    return info_switch.get(num)


def getScoreNum(num):
    score = {
        '优': 4.5,
        '良': 3.5,
        '中': 2.5,
        '及格': 1.5
    }
    return score.get(num)


def getScore(username, psw):

    s = login(username, psw)
    if s == 0:
        return 0

    # get socre
    # 成绩页面
    try:
        url_score = 'http://202.115.133.173:805/SearchInfo/Score/ScoreList.aspx'
        # # 下载成绩页面源代码
        # print(s.get(url_score).text)
        res = s.get(url_score).text
    except:
        return 0

    soup = BeautifulSoup(res, 'lxml')

    score_list = []
    type_list = [0, 2, 4, 5]
    # lis = soup.findAll('ul', {'class': 'score_right_infor_list listUl'})
    # print(lis[0])
    # exit()

    for li in soup.findAll(name='ul', attrs={'class': 'score_right_infor_list listUl'}):
        # if line_num == 0:
        #     line_num += 1
        #     continue
        info_num = 0
        # line_num = 0
        i = 0
        score_dict = {}
        for div in li.findAll('div'):
            # score_dict = {
            #     '学期': '',
            #     '课程': '',
            #     '学分': '',
            #     '成绩': ''
            # }
            # if info_num in detail_rank:
            if i in range(0, 10):
                i += 1
                continue
            info_type = getDetail(info_num)

            if info_num in type_list:
                score_detail_dict = {
                    info_type: div.text.strip()
                }
                score_dict.update(score_detail_dict)

            info_num += 1
            if info_num == 10:
                score_list.append(score_dict)
                score_dict = {}
                info_num = 0

    # print(score_list)
    score_list_dict = {'score': score_list}

    return score_list_dict

            # print(div.text.strip())
            # print('a')
        # if li.string == None:
        #     li = 'none'
        #     # print(li)
        # else:
        #     print(type(li.string.strip()))
        #     print(li.string.strip())
        #     print('a')


def getAvgScore(username, psw):
    score_list_dict = getScore(username, psw)
    if score_list_dict == 0:
        print("账户密码不正确或响应超时（成绩） ", time.ctime())
        status = {
            'status': -1,
            'description': '账户密码不正确或响应超时'}
        return status
    score_sum = 0
    credit_sum = 0
    cs_sum = 0
    for course in score_list_dict['score']:
        score = course['Score']
        if score in ['优', '良', '中']:
            gpa = getScoreNum(score)
            score = float(getScoreNum(score) * 10 + 50)
        else:
            score = float(score)
            gpa = float((int(score)-50)/10)
        credit = float(course['Credit'])
        score_sum += score
        credit_sum += credit
        cs_sum += gpa * credit
    GPA = cs_sum / credit_sum
    avg_score = score_sum / len(score_list_dict['score'])
    result = {
        '平均分': "%.1f" % avg_score,
        '平均绩点': "%.1f" % GPA
    }
    status = {
        'status': 1,
        'description': 'success'}
    score_list_dict.update(result)
    score_list_dict.update(status)
    # print(score_sum)
    # print(credit_sum)
    # print("%.1f"%GPA)
    return score_list_dict


if __name__ == "__main__":
    print(getAvgScore(''))
