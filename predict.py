# -*- coding: utf-8 -*-
import utils
import requests
import os
import sys
from requests.exceptions import HTTPError, ConnectionError, Timeout, TooManyRedirects
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score, precision_score, f1_score
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import config
import collections


current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)


import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, TooManyRedirects

def detect_one_sample(url, data):
    # 要发送的数据
    payload = {
        'data': data
    }

    headers = {
        'Content-Type': 'application/json',  # 通常POST请求的JSON数据需要设置此头部
        # ... 可以添加其他头部信息，如认证信息
    }

    # 发送POST请求
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # 如果响应不成功，HTTPError会被触发

        # 解析数据并返回
        data = response.json()
        print(data)

        value = data.get('class', None)  # 使用get来避免可能的KeyError

        return value

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except TooManyRedirects as redirects_err:
        print(f"Too many redirects: {redirects_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    return None



#
def detect_batch(url,list_of_tuples):
    '''
    url:detect url
    list_of_tuples: list of tuples  [('text','label'),('text',"label")]
    return: list of dict
    return : list of list   [[序号1，txt，y_true,y_pred],[序号2，txt，y_true,y_pred]]
    '''

    test_records = []
    # 发送请求预测标签
    index = 1
    for txt,y_true_zh in list_of_tuples:
        y_pred_zh = detect_one_sample(url,txt) # {'class': '体育'}
        record = [] #

        # print('真实标签：',y_true_zh,'预测标签：',y_pred_zh)
        #
        # res = {'txt':txt,'y_true':y_true_zh,'y_pred':y_pred_zh}
        record.append(index)
        index += 1
        record.append(txt)
        record.append(y_true_zh)
        record.append(y_pred_zh)
        test_records.append(record)

    return test_records




def get_acc(y_true,y_pred):
    accuracy = round(float(accuracy_score(y_true, y_pred)),2)
    return accuracy

def get_temperature_data(y_true,y_pred):
    # 创建一个简单的分类数据集
    list_ordinates = []

    # 计算混淆矩阵
    #  chartData = [[0, 0, 5], [0, 1, 1], [0, 2, 0],
    cm = confusion_matrix(y_true, y_pred).tolist()
    print(cm,type(cm))


    # 将混淆矩阵转换为坐标和温度值
    coordinates, temperatures = [], []
    for i in range(len(cm)):
        for j in range(len(cm[i])):
            tu = (i,j,cm[i][j])
            list_ordinates.append(tu)

            coordinates.append((i, j))
            temperatures.append(cm[i][j])

    # 打印坐标和对应的温度值

    for coord, temp in zip(coordinates, temperatures):
        print(f"坐标: {coord}, 温度值: {temp}")


    return list_ordinates

def get_matrix(y_true, y_pred):
    # 获取所有的类别标签
    '''
    y_true: list  [1,3,...]
    y_pred: list  [1,2,...]
    return [{ 'label_digit':9
                'precision': [1,2,2],
                'recall':[6,4,3].
                'f1' = 0.98
                },{...}
                ... ]
    '''


    classes = set(y_true)
    metrics = {}

    data = []

    for c in classes:
        label_zh = config.ENG2ZH[config.NUM2ENG[c]]
        res = {'类别(Category)':label_zh}
        # 算出该标签下，有几条数据
        support = y_true.count(c)
        res['测试样本数(Support)'] = support


        # True Positive (TP)
        tp = sum((y == c) and (p == c) for y, p in zip(y_true, y_pred))
        # False Positive (FP)
        fp = sum((y != c) and (p == c) for y, p in zip(y_true, y_pred))
        # True Negative (TN)
        tn = sum((y != c) and (p != c) for y, p in zip(y_true, y_pred))
        # False Negative (FN)
        fn = sum((y == c) and (p != c) for y, p in zip(y_true, y_pred))

        # Precision, Recall, and F1-Score
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

#     {'category': '体育', '精确率(precision)': '0.1', '召回率(Recall)': '4:18','F1 Score':0.8,'Support':0},
        res['精确率(precision)'] = round(precision,2)
        res['召回率(Recall)'] = round(recall,2)
        res['F1 Score'] = round(f1,2)
        data.append(res)
    print('共计算了',len(data),'条数据')
    for item in data:
        print(item)

    return data






if __name__ == '__main__':
    data = '''原题：美智库教台军对付大陆两栖登陆战环球时报特约记者：在美国“重返亚太”的军事格局下，冷战中一度被赋予“不沉航母”身份的台湾该做些什么呢？美国企业研究所（ＡＥＩ）最新发表的报告称，确保战时快速粉碎台湾意志并实施两栖登陆仍是解放军重要的斗争课题，与之相对应，对台军该如何反制大陆的“两栖闪电战”，ＡＥＩ开出了所谓“不对称药方”。据台湾“中央社”６日报道，这项题为“平衡中的亚洲：美国在亚洲军事战略的转型”的报告是由前美国国防部官员卜大年（Ｄａｎ　Ｂｌｕｍｅｎｔｈａｌ）与多名学者共同撰写，内容中有多处强调所谓“台海军力失衡”问题，进而引申出围绕“大陆对台动武门槛降低”的“担忧”。报告表示，中国大陆部署在福建、江西、广东的弹道导弹，即使在没有军事冲突发生的情形下，也足以在关键时刻动摇美国及其盟友援台的信心。报告尤其点了解放军发展的东风－２１Ｄ反舰弹道导弹的名，该导弹据说赋予解放军在距岸１５００公里外打击海上机动舰队的能力，特别是对美国航母构成严重威胁，成为中国大力构建“反介入／区域隔离”作战系统的王牌。不仅如此，中国大陆未来还将发展射程更远的反舰弹道导弹，从而进一步驱美国航母于台湾之外。报告'''
    url ='http://127.0.0.1:5001/showtag'
    xlsx_file_name = 'predictData.xlsx'

    # test_batch(url, test_samples)


    respond = detect_one_sample(data,url)
    # print(respond)

    pass



