from flask_apscheduler import APScheduler
from flask import Flask

a = {}
b = {}


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:job_1',
            'args': '',
            'trigger': 'cron',
            'hour': 14,
            'minute': 33
        },
        {
            'id': 'job2',
            'func': '__main__:job_2',
            'args': '',
            'trigger': 'cron',
            'hour': 14,
            'minute': 33
        }
    ]


def job_1():  # 一个函数，用来做定时任务的任务。
    # print(str(a) + ' ' + str(b))
    global a
    a = {2: 3}
    print('1')


def job_2():  # 一个函数，用来做定时任务的任务。
    # print(str(a) + ' ' + str(b))
    global b
    b = {5: 3}
    print('2')


app = Flask(__name__)  # 实例化flask

app.config.from_object(Config())  # 为实例化的flask引入配置


@app.route('/')  # 首页路由
def hello_world():
    global a
    print(a)
    if a == {}:
        return {1:1}
    else:
        return a


@app.route('/2')  # 首页路由
def hello_world2():
    global b
    print(b)
    if b == {}:
        return {2:2}
    else:
        return b


if __name__ == '__main__':
    scheduler = APScheduler()  # 实例化APScheduler
    scheduler.init_app(app)  # 把任务列表放进flask
    scheduler.start()  # 启动任务列表
    app.run()  # 启动flask