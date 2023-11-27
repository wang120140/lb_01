# -*- coding: utf-8 -*-
import math

import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

import ddddocr,time,os

from gevent.pywsgi import WSGIServer

ocr = ddddocr.DdddOcr()

#数据库连接

dbhost='localhost'
dbuser='root'
dbpass='!QAZ2wsx3edc'
dbname='wyh_lb'

db=pymysql.connect(host=dbhost,user=dbuser,password=dbpass,database=dbname)
cursor = db.cursor()

#后端服务启动
app = Flask(__name__)
CORS(app, resources=r'/*')

@app.route('/login/list', methods=['POST'])
def login_list():
    if request.method == "POST":
        cursor.execute("SELECT id,username,role,ctime FROM login")
        data = cursor.fetchall();
        temp = {}
        result = []
        if(data!=None):
            for i in data:
                temp["id"]=i[0]
                temp["username"]=i[1]
                temp["role"]=i[2]
                temp["ctime"]=i[3]
                result.append(temp.copy())
            print("result: ",len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])

@app.route('/login/add', methods=['POST'])
def login_add():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        try:
            cursor.execute("INSERT INTO login(username,password,role) VALUES (\""+str(username)
                +"\",\""+str(password)+"\","+str(role)+")")
            db.commit()
            print("add a new user successfully")
            return "1"
        except Exception as e:
            print("add a new user failed: ",e)
            db.rollback()
            return "-1"

@app.route('/login/del', methods=['POST'])
def login_del():
    if request.method == "POST":
        id = request.form.get("id")
        try:
            cursor.execute("DELETE FROM login WHERE id="+str(id))
            db.commit()
            print("delete the user successfully")
            return "1"
        except Exception as e:
            print("delete the user failed: ",e)
            db.rollback()
            return "-1"

@app.route('/login/update', methods=['POST'])
def login_update():
    if request.method == "POST":
        id = request.form.get("id")
        password = request.form.get("password")
        try:
            cursor.execute("UPDATE login SET password=\""+str(password)+"\" where id="+str(id))
            db.commit()
            print("update successfully")
            return "1"
        except Exception as e:
            print("update failed: ",e)
            db.rollback()
            return "-1"

@app.route("/test/w", methods=['GET'])
def test():
    print("获取成功")
    return jsonify([])


response1 = requests.get(url='http://117.39.28.234:8023/index/users/login')



response = requests.get(url='http://117.39.28.234:8023/vercode/vercode.php?a=0.9648711446576737')

with open('./1.png','wb+') as files:
    files.write(response.content)
with open('./1.png','rb') as files1:
    yu = files1.read()
ui = ocr.classification(yu)
if(len(ui) == 4):
    print(ui)
else:
    print(ui)
    print("识别错误")



# http://117.39.28.234:8023/index/users/chklogin


# print(response.content)
# print(response.text)
# print(response.reason)
# print(response.encoding)
# print(response.request.headers)
# print(response.raw)
# print(response.content)

print("---------------------------")


if __name__ == "__main__":
    # app.run(host='0.0.0.0',port=7899)
    http_server = WSGIServer(('0.0.0.0', 7899), app)
    http_server.serve_forever()
    db.close()
    print("Good bye!")
