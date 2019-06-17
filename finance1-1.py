import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np
import os, sys
from PIL import Image, ImageTk
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib
import tkinter as Tk

def crawl_finance(stockid):
    now = int(datetime.datetime.now().timestamp())+86400
    url = "https://query1.finance.yahoo.com/v7/finance/download/" + stockid + ".TW?period1=0&period2=" + str(now) + "&interval=1d&events=history&crumb=hP2rOschxO0"
    response = requests.post(url)

    with open("stockfile.csv", "w") as f:
        f.writelines(response.text)
    
    fine_stockdata = pd.read_csv("stockfile.csv", index_col = "Date", parse_dates = ["Date"])

def draw_figure(time_start,time_end):
    #將輸入的時間轉為datetime，以便後續挑選資料
    begind = datetime.datetime(int(time_start[0]),int(time_start[1]),int(time_start[2]))
    lastd = datetime.datetime(int(time_end[0]),int(time_end[1]),int(time_end[2]))
    timelast = lastd - begind
    timelast_sec = timelast.days*86400 + timelast.seconds

    #將選定時段內的資料存到清單中，且略去沒有紀錄的日期資料
    #比較每一行資料的時間，將該行資料日期減去輸入的開始日期
    #其秒數總和介在0至(結束日-開始日的秒數總和)間
    #則挑選該行資料進chose.period.csv
    list_ = []
    with open("stockfile.csv", "r") as f:
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
    with open("chose_period.csv","w") as c:
        c.write(tite)
        for element in list_:
            for i in range(len(element)):
                if i == len(element) - 1:
                    c.write(element[i])
                else:
                    c.write(element[i]+",")     
            c.write("\n")
            
    #按照輸股票代碼與時間區段製作股價趨勢圖
    with open("chose_period.csv","r") as d:
        import pandas as pd
        matplotlib.use('TkAgg')
        root =Tk.Tk()
        root.title("matplotlib in TK")
        #設定圖形的尺寸大小
        f =Figure(figsize=(5,4), dpi=100)
        a = f.add_subplot(111)
        #繪製圖形
        file = 'chose_period.csv'
        pd = pd.read_csv(file)
        y_values = pd['Close']
        x_values = pd['Date']
        x_list=[]
        y_list=[]
        for j in y_values :
            y_list.append(j)
        for i in x_values :
            x_list.append(i)
        tick_spacing = 1000000
        a.plot(x_list, y_list)

        #將繪製成功的股價圖import到tk窗口上
        canvas =FigureCanvasTkAgg(f, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        #定義並綁定鍵盤事件處理函數
        def on_key_event(event):
            print('you pressed %s'% event.key)
            key_press_handler(event, canvas, toolbar)
            canvas.mpl_connect('key_press_event', on_key_event)
        #建立結束按鈕
        def _quit():
            root.quit()
            root.destroy()
        button =Tk.Button(master=root, text='Quit', command=_quit)
        button.pack(side=Tk.BOTTOM)
        Tk.mainloop()

stockid = input('')

time_start = input('').split('/') #ex:2018/3/27

time_end = input('').split('/')

crawl_finance(stockid)
draw_figure(time_start,time_end)