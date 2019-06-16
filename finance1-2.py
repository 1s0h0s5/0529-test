import sys
import tkinter as Tk
import matplotlib
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import csv
import pandas as pd

from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
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

