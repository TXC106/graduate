# -*- coding: utf-8 -*-
# @Time : 2020/1/24
# @Author : kiwi
# @File : spider_calendar.py
# @Project : lydf
from flask import Flask, request, jsonify
from spider_calendar import getCalendar
from spider_mainpic import getMainPic
from spider_announcement import getAnnouncement
from spider_schedule import get_personal_schedule
from spider_teacher import getTeacherInfo
from spider_emptyroom import getEmptyRoom
from library_announcement import getLibAnnounce
from library_borrow import getBorrowRecord
from evaluation import getEvaluationLink
from spider_score import getAvgScore
from library_reserve import getReserved
# from library_booksearch import searchBooks
from library_booksearch_web import searchBooks
from flask_apscheduler import APScheduler
import time

pic_dict = {}
announce_dict = {}


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:pic_update',
            'args': '',
            'trigger': 'cron',
            'hour': 3,
            'minute': 0
        },
        {
            'id': 'job2',
            'func': '__main__:annouce_update',
            'args': '',
            'trigger': 'cron',
            'hour': 3,
            'minute': 0
        },
        {
            'id': 'job3',
            'func': '__main__:searchbook_start',
            'args': '',
            'trigger': 'cron',
            'hour': 21,
            'minute': 1
        }
    ]


def pic_update():
    global pic_dict
    try:
        pic_dict = getMainPic()
        # print(1)
    except:
        print("更新时页面异常", time.ctime())


def annouce_update():
    global announce_dict
    try:
        announce_dict = getAnnouncement()
        # print(2)
    except:
        print("更新时页面异常", time.ctime())


def searchbook_start():
    searchBooks('软件工程')
    print("webok")


app = Flask(__name__)  # 实例化flask

app.config.from_object(Config())  # 为实例化的flask引入配置


@app.route('/calendar', methods=['get'])
def Calendar():
    return getCalendar()


@app.route('/mainpic', methods=['get'])
def MainPic():
    global pic_dict
    if pic_dict == {}:
        pic_dict = getMainPic()
        return jsonify(pic_dict)
    else:
        # print("pic")
        return jsonify(pic_dict)


@app.route('/announce', methods=['get'])
def Announcement():
    global announce_dict
    if announce_dict == {}:
        announce_dict = getAnnouncement()
        return jsonify(announce_dict)
    else:
        # print("announce")
        return jsonify(announce_dict)


@app.route('/schedule', methods=['post'])
def Schedule():
    username = request.values.get('username', 0)
    psw = request.values.get('password', 0)
    return jsonify(get_personal_schedule(username, psw))


@app.route('/score', methods=['post'])
def Score():
    username = request.values.get('username', 0)
    psw = request.values.get('password', 0)
    return jsonify(getAvgScore(username, psw))


@app.route('/teacher', methods=['post'])
def Teacher():
    username = request.values.get('username', 0)
    psw = request.values.get('password', 0)
    t_name = request.values.get('tname', 0)
    return jsonify(getTeacherInfo(username, psw, t_name))


@app.route('/room', methods=['post'])
def Room():
    username = request.values.get('username', 0)
    psw = request.values.get('password', 0)
    b_name = request.values.get('bname', 0)
    time = request.values.get('time', 0)
    return jsonify(getEmptyRoom(username, psw, b_name, time))


@app.route('/lib_announce', methods=['get'])
def LibAnnouncement():
    return jsonify(getLibAnnounce())


@app.route('/evaluation', methods=['get'])
def Evaluation():
    return getEvaluationLink()


@app.route('/reserve', methods=['get'])
def Reserve():
    return getReserved()


# @app.route('/booksearch', methods=['post'])
# @app.route('/booksearch', methods=['get'])
def SearchBooks():
    # bookname = request.values.get('bname', 0)
    # return searchBooks(bookname)
    searchBooks('软件工程')


@app.route('/lib_record', methods=['post'])
def LibRecord():
    username = request.values.get('username', 0)
    psw = request.values.get('password', 0)
    return jsonify(getBorrowRecord(username, psw))


# @app.route('/avg_score', methods=['post'])
# def AvgScore():
#     username = request.values.get('username', 0)
#     psw = request.values.get('password', 0)
#     return jsonify(getAvgScore(username, psw))


if __name__ == "__main__":
    scheduler = APScheduler()  # 实例化APScheduler
    scheduler.init_app(app)  # 把任务列表放进flask
    scheduler.start()  # 启动任务列表
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=5000, debug=False)
