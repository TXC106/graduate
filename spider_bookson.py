from flask import Flask, request, jsonify
from library_booksearch_web import searchBooks
from flask_apscheduler import APScheduler

class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:searchbook_start',
            'args': '',
            'trigger': 'cron',
            'hour': 10,
            'minute': 32
        }
    ]


def searchbook_start():
    searchBooks('软件工程')
    print("webok")

app = Flask(__name__)  # 实例化flask

app.config.from_object(Config())  # 为实例化的flask引入配置

@app.route('/', methods=['get'])
def Search():
	return '0.0.0.0:7788'

if __name__ == "__main__":
    scheduler = APScheduler()  # 实例化APScheduler
    scheduler.init_app(app)  # 把任务列表放进flask
    scheduler.start()  # 启动任务列表
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=5050, debug=False)
