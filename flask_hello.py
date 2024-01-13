# -*- coding: utf-8 -*-
import logging
import sys

print(sys.path)

from glob import escape

from flask import Flask, render_template, jsonify, request
from predictor import Predictor

# flask版本为: pip install flask==2.3.3
app = Flask(
    __name__,
    static_folder="static",  # 给定静态文件保存的文件夹路径
    template_folder="templates"  # 给定html页面的保存文件夹路径
)
predictor = Predictor()

app.json.ensure_ascii = False  # 当前flask版本有效，给定json格式数据返回的时候，针对中文不进行编码处理


@app.route("/")
@app.route("/index")
def index():
    # noinspection PyUnresolvedReferences
    return render_template("index.html")


@app.route("/hello")
def hello_world():
    return "<p>Hello, World!我是小明o</p>"


@app.route("/weapi/copyright/pay_fee_message/config")
def pay_fee_message_config():
    rst = {"code": 200, "config": {"vip": "版权方要求，当前歌曲需付费使用，开通VIP即可自由畅享"}}
    return jsonify(rst)


@app.route('/user/<username>')
@app.route('/user')
def show_user_profile(username='未知'):
    # show the user profile for that user
    print(type(username))
    return f'User {escape(username)}'


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    print(type(post_id))
    return f'Post {post_id}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    print(type(subpath))
    return f'Subpath {escape(subpath)}'


def do_the_login():
    print("执行login操作")
    username = request.form.get('username')
    password = request.form.get('password')
    # NOTE: 执行的具体的登录逻辑
    return f"login successful:{username} - {password}"


def show_the_login_form():
    # noinspection PyUnresolvedReferences
    # value = request.args.get('key')
    return render_template("login.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


@app.route("/predict1/<float:age>/<float:gender>/<float:height>/<float:weight>")
def predict1(age, gender, height, weight):
    r = predictor.predict(age, gender, height, weight)  # 调用模型获取预测结果
    return jsonify({
        'code': 200,
        'data': r
    })


@app.route("/predict2", methods=['GET', 'POST'])
def predict2():
    try:
        # 参数获取&参数检查&参数类型转换....
        if request.method == 'GET':
            _args = request.args
        else:
            _args = request.form
        age = float(_args['age'])
        gender = float(_args['gender'])
        height = float(_args['height'])
        weight = float(_args['weight'])
        r = predictor.predict(age, gender, height, weight)  # 调用模型获取预测结果
        return jsonify({
            'code': 200,
            'data': r
        })
    except Exception as e:
        logging.error("服务器模型预测异常.", exc_info=e)
        return jsonify({
            'code': 201,
            'msg': f'服务器异常:{e}'
        })


if __name__ == '__main__':
    # 也可以直接命令行执行: flask --app flask_hello run
    # 0.0.0.0特殊IP地址，表示当前机器的所有IP地址
    # 127.0.0.1特殊IP地址,表示当前机器的IP(本地IP)
    # 局域网IP地址：仅共局域网内部机器互相访问的IP地址, A类(10.xx)、B类(172.xx)、C类(192.168.xxx)
    # 公网IP地址：提供互联网访问的IP地址
    app.run(
        host="0.0.0.0",  # 给定服务监听的ip地址
        port=5000,  # 给定服务监听的端口号False
        debug=True  # 当debug为True的时候，表示当代码进行更改后，会重新的进行服务的启动
    )
