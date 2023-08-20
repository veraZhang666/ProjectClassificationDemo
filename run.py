from flask import Flask,url_for,render_template,request,jsonify,send_from_directory

import base64
import json
import sys,os
import utils
import predict
import config

current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)

app = Flask(__name__)

# 1.接收前端发来的xlsx文件并解析
# 2.审核格式是否正确
# 3.格式不正确，返回空
# 4. 格式正确，返回预测结果数据,前端解析并展示
@app.route('/upload', methods=['POST'])
def upload_file():
    print(request.files)
    print('---------------------------------------')
    # 获取 "data" 文件输入字段
    file = request.files.get('data')

    response = {'data': '',
                'message': ""
                }

    if not file:
        response['message'] =  "上传文件为空。"
        return jsonify(response)

    if not file.filename.endswith('.xlsx'):
        response['message'] =  '文件类型不对,请上传xlsx文件。'
        return jsonify(response)

    # 使用 openpyxl 加载并读取文件
    # TODO 用前端接收过来的xlsx代替！！！！
    # xlsx_file_path = r'C:\Users\admin\Dropbox\demoBackEnd\mywebsite\uploads\predictData.xlsx'
    xlsx_file_path = file
    list_of_tuples = utils.read_xlsx_excel(xlsx_file_path)

    # 3.格式不正确，返回空
    if list_of_tuples == None:
        response['message'] = '检查xlsx文件数据填写有误，请按照模板提供的要求填写。'
        return jsonify(response)

    # 3.格式正确，每一条数据发送请求
    else:
        # 调用批量预测方法，拿到返回结果,[]
        # TODO 用模型预测模块代替！！！！
        url = 'http://127.0.0.1:5001/showtag' # 模型预测的url
        detect_result = predict.detect_batch(url,list_of_tuples)


        # 计算acc
        y_true,y_pred = utils.labelZH2digit(detect_result)
        acc = predict.get_acc(y_true=y_true,y_pred=y_pred)

        # 计算 matrix
        # 计算heatmap
        x_y_axis = config.LABELS
        matrix_data = predict.get_matrix(y_true=y_true,y_pred=y_pred)

        heatmap_data = predict.get_temperature_data(y_true=y_true,y_pred=y_pred)

        # detect_result = [("预测内容","标签","预测结果"),('这是关于体育的新闻内容','体育','体育'),('这是关于财经的新闻内容','财经','财经')]

        xlsx_header = ['序号','预测文本','真实标签','预测结果']
        detect_result.insert(0,xlsx_header)
        response = {
                    'result': {
                            'acc': acc,
                            'matrix': matrix_data,
                            "heatmap": {
                                        "axis": x_y_axis,
                                        "heatmap_data": heatmap_data
                                        },
                            "detect_result":detect_result
                             },
                    'message':'识别成功！'
                    }
        print(response)


        print('=====================')
        # return jsonify(json.dumps(response))
        return response






@app.route('/')
def index():
    return render_template('index.html')



@app.route('/showtag',methods=['GET','POST'])
def show_tag():
    dic = {'class':'体育'}
    return jsonify(dic)

@app.route('/gettemplate')
def get_template():
    xlsx_file_path = os.path.join('xlsxTemplate','template.xlsx')
    print(xlsx_file_path)
    return send_from_directory(path=xlsx_file_path, directory='xlsxTemplate', filename='template.xlsx',
                               as_attachment=True)





if __name__=='__main__':
	app.run(host='127.0.0.1',port =5000)












