# -*- coding: utf-8 -*-
# @Time : 2020/2/11
# @Author : kiwi
# @File : avg_score.py
# @Project : spider
from spider_score import getScore


def getScoreNum(num):
    score = {
        '优': 4.5,
        '良': 3.5,
        '中': 2.5,
    }
    return score.get(num)


def getAvgScore(username, psw):
    score_list_dict = getScore(username, psw)
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
    # print(score_sum)
    # print(credit_sum)
    # print("%.1f"%GPA)
    return result


if __name__ == "__main__":
    getAvgScore('201712090414', '420502199704251123')
