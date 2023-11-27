# 获取Image后台

from w02 import getMyCookie  # 获取单个cookie值
from w03 import readExcel  # 读取表格数值

import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS
from gevent.pywsgi import WSGIServer

_av = readExcel()  # 获取表格里面具体信息内容

app = Flask(__name__)
CORS(app, resources=r'/*')

# 改变dic 转成str
def changeStr(pram_):
    a_sing = ""
    for key, values in pram_.items():
        b_sing = key + "=" + values + "; "
        a_sing += b_sing
    return a_sing


@app.route("/test/w", methods=['GET'])
def test():
    # 获取 json 类型数据:
    json_bytes = int(request.args["id"])
    user_msg = _av["useValue"][json_bytes]

    result1 = getMyCookie(user_msg)
    while result1 is None:
        print("**************none****************")
        result1 = getMyCookie(user_msg)
    print(result1)
    user_msg["cookie_valie"] = changeStr(result1.get("data"))
    user_msg["status"] = result1["status"]
    print(user_msg)
    print("获取成功")
    return jsonify(user_msg)


if __name__ == "__main__":
    # app.run(host='0.0.0.0',port=7899)
    http_server = WSGIServer(('0.0.0.0', 7899), app)
    http_server.serve_forever()
    # db.close()
    print("Good bye!")
