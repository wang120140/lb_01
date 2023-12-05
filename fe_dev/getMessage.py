
# -*- coding: utf-8 -*-
import random
from datetime import datetime
from init_db import connector
from flask import Flask, request, jsonify
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
import logging
# 初始化连接
app = Flask(__name__)
CORS(app, resources=r'/*')

def request_parse(req_data):
	#'''解析请求数据并以json形式返回'''
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data

@app.route("/test/w", methods=['GET'])
def test():
    result = connector.execute("SELECT * FROM msg_base_sg")

    return jsonify(result)

@app.route("/getMessageList",methods=['POST'])
def getMessageList():
    data=request_parse(request)
    start = (data["pageNum"]-1)*data["pageSize"]
    print(start)
    print(data)
    try:
        result = connector.execute("SELECT * FROM msg_base_sg LIMIT %s OFFSET %s  ",(data["pageSize"], start))
        resultNum = connector.execute("SELECT COUNT(*) as num FROM msg_base_sg  ")
        print(resultNum)
    except Exception as e:
        print(e)
        result = []
    finally:
        print("结束")
        print(result)
    if result is None :
        return []
    else:
        return {
            "num":resultNum[0]['num'],
            "arr":result
        }
if __name__ == "__main__":
    # app.run(host='0.0.0.0',port=7899)
    http_server = WSGIServer(('0.0.0.0', 7999), app)
    http_server.serve_forever()
    # db.close()
    print("Good bye!")

















def test_m ():
    # 插入单行数据
    data = {'name': 'Alice', 'age': 20, 'created_at': datetime.now()}
    connector.insert('users', data)

    # 插入多行数据
    data_list = [{'name': 'Bob', 'age': 25, 'created_at': datetime.now()},
                 {'name': 'Charlie', 'age': 30, 'created_at': datetime.now()}]
    connector.insert_many('users', data_list)

    # 查询数据
    result = connector.execute("SELECT * FROM users")
    print(result)

    # 查询单条数据
    result = connector.query_one("SELECT * FROM users WHERE name = %s", ('Alice',))
    print(result)

    # 查询多条数据
    result = connector.execute("SELECT * FROM users WHERE age > %s", (25,))
    print(result)

    # 更新数据
    data = {'age': random.randint(20, 40)}
    where_clause = "name = %s"
    connector.update('users', data, where_clause)

    # 删除数据
    where_clause = "age < %s"
    connector.delete('users', where_clause)