# -*- coding: utf-8 -*-
import copy
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
    # '''解析请求数据并以json形式返回'''
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data


@app.route("/test/w", methods=['GET'])
def test():
    result = connector.execute("SELECT * FROM msg_base_sg")

    return jsonify(result)


@app.route("/getMessageList", methods=['POST'])
def getMessageList():
    global query_1
    data = request_parse(request)
    start = (data["pageNum"] - 1) * data["pageSize"]
    _k = "王"
    my_sql = []
    my_query = []
    try:
        # query =  "SELECT * FROM msg_base_sg LIMIT %s OFFSET %s WHERE xing_ming LIKE %s "
        if (data["xing_ming"] == '') and (data["gong_hao"] == '') and (data["wei_xin"] == '') and (
                data["gong_zhong"] == '') and (
                data["is_my"] == ''):
            query = "SELECT * FROM msg_base_sg   "
            query_1 = "SELECT COUNT(*) as num FROM msg_base_sg  "
        else:
            query = "SELECT * FROM msg_base_sg    WHERE "
            query_1 = "SELECT COUNT(*) as num FROM msg_base_sg  WHERE "
        if data["xing_ming"] != '':
            my_sql = my_sql + [" xing_ming LIKE %s "]
            my_query = my_query + ['%' + data["xing_ming"] + '%']
        if data["gong_hao"] != '':
            my_sql = my_sql + [" gong_hao LIKE %s "]
            my_query = my_query + ['%' + data["gong_hao"] + '%']
        if data["wei_xin"] != '':
            my_sql = my_sql + [" wei_xin LIKE %s "]
            my_query = my_query + ['%' + data["wei_xin"] + '%']
        if data["is_my"] != '':
            my_sql = my_sql + [" is_my LIKE %s "]
            my_query = my_query + ['%' + data["is_my"] + '%']
        if data["gong_zhong"] != '':
            my_sql = my_sql + [" gong_zhong LIKE %s "]
            my_query = my_query + ['%' + data["gong_zhong"] + '%']
        # result = connector.execute(query,(data["pageSize"], start, '%' + _k + '%',))
        print(my_sql)
        if len(my_sql) == 0:
            query = query + " LIMIT %s OFFSET %s"
        elif len(my_sql) == 1:

            query = query + my_sql[0] + " LIMIT %s OFFSET %s"
            query_1 = query_1 + my_sql[0]
        else:
            co_ = 'AND '.join(my_sql)
            query = query + co_ + " LIMIT %s OFFSET %s"
            query_1 = query_1 + co_
        my_query_1 = copy.deepcopy(my_query)
        my_query = my_query + [data["pageSize"], start, ]

        result = connector.execute(query, tuple(my_query))
        resultNum = connector.execute(query_1, tuple(my_query_1))
        print(resultNum)
    except Exception as e:
        print(e)
        result = []
    finally:
        print("结束")
        print(result)
    if result is None:
        return []
    else:
        return {
            "num": resultNum[0]['num'],
            "arr": result
        }


@app.route("/updataOrAdd", methods=['POST'])
def updataOrAdd():
    data_1 = request_parse(request)
    query_1 = 'INSERT INTO msg_base_sg(xing_ming, gong_hao, mi_ma, wei_xin, gong_zhong, fen_shu, mi_is_right, is_year, is_my, cookie_value, is_continue, is_timeout) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    my_query_1 = [data_1["xing_ming"], data_1["gong_hao"], data_1["mi_ma"],
                  data_1["wei_xin"], data_1["gong_zhong"], data_1["fen_shu"],
                  data_1["mi_is_right"], data_1["is_year"], data_1["is_my"],
                  "1", "1", "1"
                  ]

    data_1["cookie_value"] = "1"
    data_1["is_continue"] = "1"
    data_1["is_timeout"] = "1"

    # result_1 = connector.insert(query_1, tuple(my_query_1))
    # connector.commit()
    # print(result_1)

    result_1 = connector.execute("SELECT * FROM msg_base_sg WHERE gong_hao = %s", (data_1["gong_hao"],))
    print(result_1)
    if len(result_1) >= 1:
        where_clause = "gong_hao = %s"
        connector.update('msg_base_sg', data_1, where_clause, [data_1["gong_hao"]])
        return {"code": "200", "msg": "成功"}
    else:
        connector.insert('msg_base_sg', data_1)
        return {"code": "200", "msg": "成功"}


@app.route("/deletItem", methods=['POST'])
def deletItem():
    data_1 = request_parse(request)
    where_clause = f"gong_hao = '{data_1['gong_hao']}'"
    # connector.delete('msg_base_sg', where_clause, data_1['gong_hao'])

    result = connector.execute("DELETE FROM msg_base_sg WHERE gong_hao = %s", (data_1['gong_hao'],))
    print(result)
    return {}


if __name__ == "__main__":
    # app.run(host='0.0.0.0',port=7899)
    http_server = WSGIServer(('0.0.0.0', 7999), app)
    http_server.serve_forever()
    # db.close()
    print("Good bye!")


def test_m():
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
