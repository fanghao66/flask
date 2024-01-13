# flask

## 1.创建一个flask对象

```undefined
from flask import Flask
app = Flask(
    __name__,
    static_folder="static",  # 给定静态文件保存的文件夹路径
    template_folder="templates"  # 给定html页面的保存文件夹路径
)
```

## 2.flask的运行

**http url的组成**

	eg:https://baike.baidu.com:443/item/HTTP/243074?fr=ge_ala&k2=v2

	协议：https

	域名：baike.baidu.com

	端口号：https默认端口443，http默认端口80

	路由：item/HTTP/243074

	参数部分：key/value(fr=ge_ala&k2=v2)

### 2.1 app.run(host,port,debug)

**监听的IP地址设置**

		0.0.0.0 本地所有的IP地址

		127.0.0.1特俗IP地址，表示当前机器的IP（本地IP）

		局域网IP地址：仅供局域网内部机器互相访问的IP地址，例如​`, A类(10.xx)、B类(172.xx)、C类(192.168.xxx)`​

		公网IP地址：提供互联网访问的IP地址

**端口号设置一般是10000~50000**

**Debug设置，True的情况下有修改自动重启。**

### 2.2 路由设置

	@app.route(path,methods=[])

**path为相对于当前IP+端口的位置**

**methods为一个列表通过request.method获取**

#### 2.2.1 静态路由

```undefined
@app.route("/hello")
def hello_world():
    return "<p>Hello, World!我是小明o</p>"
```

#### 2.2.2 动态路由

动态路由通过在静态地址后加<>实现，定义函数的时候需要把该动态参数，定义为函数参数。

**动态字符串**

```undefined
@app.route('/user/<username>')
def show_user_profile(username='未知'):
    # show the user profile for that user
    print(type(username))
    return f'User {escape(username)}'
```

**动态整数id**

```undefined
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    print(type(post_id))
    return f'Post {post_id}'
```

**动态子IP**

```undefined
@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    print(type(subpath))
    return f'Subpath {escape(subpath)}'
```

#### 2.2.3 请求方式

**动态路由可以用于做请求**

```undefined
@app.route("/predict1/<float:age>/<float:gender>/<float:height>/<float:weight>")
def predict1(age, gender, height, weight):
    r = predictor.predict(age, gender, height, weight)  # 调用模型获取预测结果
    return jsonify({
        'code': 200,
        'data': r
    })
```

**GET和POST做请求(from flask import request)**   
            GET请求的时候参数在：request.args 字典中，get请求在路由地址之后，通常用？隔开，参数与参数之间用&连接，参数和传入参数的值之间用=连接。

            POST请求的时候参数在：request.form 字典中，Post请求包含表单参数和键值的处理。

```undefined
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
```

## 3.flask的返回设置

**如果是页面类型的，直接通过flask的API返回，eg: render_template**

```undefined
from flask render_template
@app.route("/index.html")
def index():
    # noinspection PyUnresolvedReferences
    return render_template("index.html")
```

**如果是普通的类型，eg:字符串、数值，可以直接return返回**

```undefined
@app.route("/hello")
def hello_world():
    return "<p>Hello, World!我是小明o</p>"
```

**如果是返回json格式数据，直接通过jsonfiy将字典对象转换为json格式并返回**

```undefined
from flask import jsonify
@app.route("/weapi/copyright/pay_fee_message/config")
def pay_fee_message_config():
    # TODO: 这里地方应该存在部分逻辑代码
    rst = {"code": 200, "config": {"vip": "版权方要求，当前歌曲需付费使用，开通VIP即可自由畅享"}}
    return jsonify(rst)
```

‍
