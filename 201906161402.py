def crawl_finance(stockid):
    import requests
    import datetime
    import pandas as pd
    import matplotlib.pyplot as plt
    now = int(datetime.datetime.now().timestamp())+86400
    url = "https://query1.finance.yahoo.com/v7/finance/download/" + stockid + ".TW?period1=0&period2=" + str(now) + "&interval=1d&events=history&crumb=hP2rOschxO0"
    response = requests.post(url)

    with open("C:\\Users\\anan2\\Desktop\\stockfile.csv", "w") as f:
        f.writelines(response.text)
    
    import pandas as pd
    fine_stockdata = pd.read_csv("C:\\Users\\anan2\\Desktop\\stockfile.csv", index_col = "Date", parse_dates = ["Date"])

def draw_figure(time_start,time_end):
    #將輸入的時間轉為datetime，以便後續挑選資料
    import datetime
    begind = datetime.datetime(int(time_start[0]),int(time_start[1]),int(time_start[2]))
    lastd = datetime.datetime(int(time_end[0]),int(time_end[1]),int(time_end[2]))
    timelast = lastd - begind
    timelast_sec = timelast.days*86400 + timelast.seconds

    #將選定時段內的資料存到清單中，且略去沒有紀錄的日期資料
    #比較每一行資料的時間，將該行資料日期減去輸入的開始日期
    #其秒數總和介在0至(結束日-開始日的秒數總和)間
    #則挑選該行資料進chose.period.csv
    import csv
    list_ = []
    with open("C:\\Users\\anan2\\Desktop\\stockfile.csv", "r") as f:
        tite = f.readline()
        a = csv.reader( f )
        for aline in a:
            oneday = aline[0].split('-')
            oned = datetime.datetime(int(oneday[0]),int(oneday[1]),int(oneday[2]))
            diff = oned - begind
            diff_sec = diff.days*86400 + diff.seconds
            if 0 <= diff_sec <= timelast_sec and aline[1] != 'null':
                list_.append( aline )
        
                
    #前一個statement將所存下的資料放到CSV中，以便後面製圖
    with open("C:\\Users\\anan2\\Desktop\\chose_period.csv","w") as c:
        c.write(tite)
        for element in list_:
            for i in range(len(element)):
                if i == len(element) - 1:
                    c.write(element[i])
                else:
                    c.write(element[i]+",")     
            c.write("\n")
            
    #按照輸股票代碼與時間區段製作股價趨勢圖
    import pandas as pd
    with open("C:\\Users\\anan2\\Desktop\\chose_period.csv","r") as d:
        e = pd.read_csv("C:\\Users\\anan2\\Desktop\\chose_period.csv", index_col = "Date", parse_dates = ["Date"])
        import matplotlib.pyplot as plt
        import numpy as np
        import os, sys
        from PIL import Image, ImageTk
        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        e.Close.plot()
        stock_time_price = 'C:\\Users\\anan2\\Desktop\\stock.png'
        if os.path.isfile(stock_time_price):
            os.remove(stock_time_price)
            plt.savefig(stock_time_price)
        else:
            plt.savefig(stock_time_price)

stockid = input('')

time_start = input('').split('/') #ex:2018/3/27

time_end = input('').split('/')

crawl_finance(stockid)
draw_figure(time_start,time_end)