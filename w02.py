# -*- coding: utf-8 -*-
# 这个方法是作用是 1.识别验证码  2.登录成功 3. 放回cookie值
import ddddocr
import requests
import time
import hashlib
ocr = ddddocr.DdddOcr()
#cegsn7bhrjnc7mk5jgo9f8kbd3
#fnvjefl0sb133r5i52s6t2qpu2
from  md5 import md5Value

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Cookie": "PHPSESSID=cegsn7bhrjnc7mk5jgo9f8kbd3",
}


def getMyCookie(pram_):
    print("--------------0获取页面信息---------------")
    response1 = requests.get(url='http://117.39.28.234:8023/index/users/login', headers=header)
    print("--------------1获取验证码---------------")
    response = requests.get(url='http://117.39.28.234:8023/vercode/vercode.php?a=0.9648711446576737', headers=header)
    # time.sleep(2)
    print("--------------2开始识别验证码---------------")
    with open('./1.png', 'wb+') as files:
        files.write(response.content)
    with open('./1.png', 'rb') as files1:
        yu = files1.read()
    ui = ocr.classification(yu)

    print("--------------3发送登录信息---------------")

    response2 = requests.post("http://117.39.28.234:8023/index/users/chklogin", {
        "username": pram_["username"],
        "password": md5Value(pram_["username"],pram_["password"]),
        "vercode": ui
    }, headers=header)
    if response2.status_code == 200:
        print(response2.json())
        getMsg = response2.json()
        print(type(getMsg))
        if getMsg["status"] == 1:  # 成功
            # 成功
            print("--------------4开始解析cookie信息内容---------------")
            cookie1 = requests.utils.dict_from_cookiejar(response2.cookies)
            res = {
                "status": 1,
                "data": cookie1
            }
            print(cookie1)
            print("--------------5完成解析cookie信息---------------")
            return res
        elif getMsg["status"] == 0:  # 失败  密码错误
            print("----密码错误---")
            res = {
                "status": 0,
                "data": {
                    "msg": "密码错误"
                },
            }
            return res
        elif getMsg["status"] == 2:  # 失败  验证码错误
            print("----验证码错误-----")
            # getMyCookie(pram_)
            return


