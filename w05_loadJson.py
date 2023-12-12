# 读取execl 表格

# 1.导入pandas模块
import pandas as pd
import datetime

now = datetime.datetime.now()
formatted_date = now.strftime("%Y-%m-%d")

# 3.读取excel的某一个sheet

    #df = pd.read_excel('./2023年_06.xlsx', sheet_name='6月答'
df = pd.read_excel(formatted_date+"_cookie.xlsx", sheet_name='Sheet1')
    #df = pd.read_excel('./炼钢.xlsx', sheet_name='2023_02')

    # df = pd.read_excel('./2023年_06_cookie.xlsl',sheet_name='Sheet1')
list_a = []
for i in df.index:
       
    list_a.append(str(df["cookieValue"][i]))
print(list_a)
    