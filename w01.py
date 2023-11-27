from w02 import getMyCookie  # 获取单个cookie值
from w03 import readExcel  # 读取表格数值
import pandas as pd
import datetime
allValue_w1 = readExcel()  # 读取excl表格信息内容

now = datetime.datetime.now()
formatted_date = now.strftime("%Y-%m-%d")
# 改变dic 转成str
def changeStr(pram_):
    a_sing = ""
    for key, values in pram_.items():
        b_sing = key + "=" + values + "; "
        a_sing += b_sing
    return a_sing


# 获取前几个的cookie
# 0------29
# 29-----40
# 40 ----56
# 56 ----90
# 90----130
# 130---146
# 146---167
# 167---197
# 201---203
#

# 这个函数作用是： 获取cookie值 然后写道excl表格中
for i in range(0,56):
    # 获取cookie值
    result1 = getMyCookie(allValue_w1["useValue"][i])
    # 如果获取失败 重新获取cookie值
    while result1 is None:
        print("**************none****************")
        result1 = getMyCookie(allValue_w1["useValue"][i])
    # 获取的cookie值转换成str值得内容信息
    val_coolie = changeStr(result1.get("data"))
    allValue_w1["allValue"]["cookieValue"][i] = val_coolie
    marks_data = pd.DataFrame(allValue_w1["allValue"])
    marks_data.to_excel(formatted_date+"_cookie.xlsx")

# 导出Excel


print("---------单个页面结束信息-------------")
