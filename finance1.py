#https://www.finlab.tw/%E7%94%A8%E7%88%AC%E8%9F%B2%E7%88%AC%E5%85%A8%E4%B8%96%E7%95%8C%E8%82%A1%E5%83%B9/

import requests
site = "https://query1.finance.yahoo.com/v7/finance/download/2330.TW?period1=0&period2=1549258857&interval=1d&events=history&crumb=hP2rOschxO0"
response = requests.post(site)
# print(response.text)
# with open("file.csv", "w") as f:
#     f.writelines(response.text)

import pandas as pd
a = pd.read_csv("file.csv")
#印出前5列
# print(a.head())

#把Date換成第一行
#其中index_col就是將Date這條column當作是index，而parse_dates可以將Date轉換成程式瞭解的日期格式，而非單純的字串。
b = pd.read_csv("file.csv", index_col = "Date", parse_dates = ["Date"])
# print(b.head())

#印出歷史股價
import matplotlib.pyplot as plt

#把b化成圖
b.Close.plot()

#顯示畫出來的圖
plt.show()
