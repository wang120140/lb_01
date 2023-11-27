# 这个是读取excel表格后 把数据输入到数据库中

# 1.导入pandas模块
import pandas as pd
# 3.读取excel的某一个sheet
def readExcel():
    #df = pd.read_excel('./2023年_06.xlsx', sheet_name='6月答'
    df = pd.read_excel('../2023年9月.xlsx', sheet_name='8月')
    list_a = []
    for i in df.index:
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