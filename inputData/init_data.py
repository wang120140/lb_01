# 这个是读取excel表格后 把数据输入到数据库中

# 1.导入pandas模块
import pandas as pd
import pdb
from tqdm import tqdm
import pymysql
from sshtunnel import SSHTunnelForwarder

# 3.读取excel的某一个sheet
def readExcel():
    li = []
    li_year = []
    df = pd.read_excel('./2023年9月.xlsx', sheet_name='8月',keep_default_na=False)
    # df = pd.read_excel('./炼钢.xlsx', sheet_name='2023_02',keep_default_na=False)
    list_a = [df.index]
    # print(dir(df))
    # pdb.set_trace() 

    for i in tqdm(df.index):
        a = {
            "index_wc": str(df["微信号"][i]),
            "username": str(df["账号"][i]),
            "password": str(df["密码"][i]),
            "_score": str(df["分数"][i]),
            "_u": str(df["姓名"][i]),
            "cookie_valie": "",
        }
        list_a.append(a)
        if( df['工种'][i] == "") :
            df['工种'][i] = "安全"
        li.append((
            str(df["微信号"][i]),# 微信号
            str(df["工种"][i]),#工种
            str(df["姓名"][i]),#姓名
            str(df["账号"][i]),#账号
            str(df["密码"][i]),#密码
            str(df["分数"][i]),#分数
            str("待更新cookie"),#cookie
            str("1"),#密码是否对的
            str("1"),#是否包年
            str("1"),#是否继续
            str("0"),#是否超时
            str("1"),#是否从我这来得
        ))
        li_year.append((
            str(df["账号"][i]),#账号
            str(df["姓名"][i]),#姓名
            str(df["微信号"][i]),# 微信号
            str("0"),
            str("0"),
            str("0"),
            str("0"),
            str("0"),
            str("0"),
            str("0"),
            str("0"),
            str("0"),
            str("0"),
            str("0"),
            str("0"),
        ))
    return {
        # "allValue": df,
        # "useValue": list_a,
        "db_List":li,
        "db_year":li_year
    }


# 配置连接参数
host = "localhost"
port = 3306
user = "root"
password = "CaZRPEejMKGE5TmG"
database = "my_lb"

# 代理参数设置
proxyHost = "152.136.45.25"
proxyPort = "22"
proxyUser = "root"
proxyPass = "wyh07143612@CSY"
charset = 'utf8mb4'

# 建立数据库连接
def mysql_base_msg(cursor_p,pram):
     cursor_p.executemany(""" insert into msg_base_sg(
                        wei_xin,
                        gong_zhong,
                        xing_ming,
                        zhang_hao,
                        mi_ma,
                        fen_shu,
                        cookie_value,
                        mi_is_right,
                        is_year,
                        is_continue,
                        is_timeout,
                        is_my) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", pram)
def mysql_base_year(cursor_p,pram):
     cursor_p.executemany(""" insert into year_2024_sg(                     
                        zhang_hao,
                        xing_ming,
                        wei_xin,
                        m1,
                        m2,
                        m3,
                        m4,
                        m5,
                        m6,
                        m7,
                        m8,
                        m9,
                        m10,
                        m11,
                        m12) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", pram)
     
try:

    server = SSHTunnelForwarder(
        ssh_address_or_host=(proxyHost, 22),  # 指定ssh登录的跳转机的address
        ssh_username = proxyUser,  # 跳转机的用户
        ssh_password= proxyPass ,  # 跳转机的密码
        remote_bind_address=(host, 3306))
    server.start()
    conn = pymysql.connect(host=host, port=server.local_bind_port, user=user, password=password, database=database,charset=charset)
    cursor =conn.cursor(cursor=pymysql.cursors.DictCursor)
    
    print("数据库连接成功！")
    all_msg=readExcel()
    print("数据读取完毕")
    mysql_base_year(cursor,all_msg["db_year"])
    # mysql_base_msg(cursor,all_msg["db_List"])
    print("数据库插入完毕")
    # 向数据库中插入内容
    conn.commit()
    # 断开
    conn.close()
  
except pymysql.Error as e:
    print("数据库连接失败：", e)


