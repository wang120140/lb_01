# 这个是读取excel表格后 把数据输入到数据库中

# 1.导入pandas模块
import pandas as pd
import pdb
from tqdm import tqdm
import pymysql
from sshtunnel import SSHTunnelForwarder


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
try:

    server = SSHTunnelForwarder(
        ssh_address_or_host=(proxyHost, 22),  # 指定ssh登录的跳转机的address
        ssh_username = proxyUser,  # 跳转机的用户
        ssh_password= proxyPass ,  # 跳转机的密码
        remote_bind_address=(host, 3306))
    server.start()


    conn = pymysql.connect(host=host, port=server.local_bind_port, user=user, password=password, database=database,charset=charset)
    
    cursor =conn.cursor()
    print("数据库连接成功！")
    
   
    
except pymysql.Error as e:
    print("数据库连接失败：", e)

# 3.读取excel的某一个sheet
def readExcel():
    #df = pd.read_excel('./2023年_06.xlsx', sheet_name='6月答'
    df = pd.read_excel('./2023年9月.xlsx', sheet_name='8月')
    list_a = [df.index]
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
    return {
        "allValue": df,
        "useValue": list_a,
    }
