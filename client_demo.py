# -*- coding: utf-8 -*-

import requests

url = "http://127.0.0.1:5000/predict2"
response = requests.post(url, data={
    'age': 12,
    'gender': 1,
    'height': 150,
    'weight': 50
})
if response.status_code == 200:
    print(response.json())  # 服务器正常返回了(预测成功或者预测失败)
else:
    print("网络异常!!!")
