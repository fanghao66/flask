# -*- coding: utf-8 -*-
from typing import Dict, Any
import numpy as np


class Predictor(object):
    def __init__(self):
        super(Predictor, self).__init__()

        self.age_scaler = [25, 10]
        self.height_scaler = [175, 20]
        self.weight_scaler = [100, 32]
        self.coef = [0.5, -0.68, -0.25, 0.68, -0.25]

    def predict(self, age: float, gender: float, height: float, weight: float) -> Dict[str, Any]:
        """
        基于给定的年龄、性别、身高、体重预测当前样本对应的用户是否身体异常，并返回是否异常的置信度概率值
        :param age: 年龄
        :param gender: 性别
        :param height: 身高
        :param weight: 体重
        :return: {'class':'异常 or 正常', 'proba':异常的概率值}
        """
        age = (age - self.age_scaler[0]) / self.age_scaler[1]
        height = (height - self.height_scaler[0]) / self.height_scaler[1]
        weight = (weight - self.weight_scaler[0]) / self.weight_scaler[1]
        score = age * self.coef[0] + gender * self.coef[1] + \
                height * self.coef[2] + weight * self.coef[3] + self.coef[4]
        if score > 0:
            return {
                'class': '异常',
                'proba': float(1.0 / (1 + np.exp(-score)))
            }
        else:
            return {
                'class': '正常',
                'proba': float(1.0 / (1 + np.exp(-score)))
            }


if __name__ == '__main__':
    predictor = Predictor()
    print(predictor.predict(25, 0, 175, 100))
    print(predictor.predict(25, 1, 175, 100))
    print(predictor.predict(25, 0, 175, 150))
    print(predictor.predict(25, 1, 200, 150))
