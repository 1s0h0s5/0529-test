
# coding: utf-8

# In[2]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import webbrowser
import xlrd
from xlrd import open_workbook
import os.path
import os
os.environ["LANG"] = "en_US.UTF-8"
import pdb
import csv

import pandas as pd
import itertools
import time
from random import randrange, uniform
import datetime
import config
import datetime
import requests
from bs4 import BeautifulSoup

import tkinter as tk
import tkinter.font as tkFont


#part2: 抓網頁、爬蟲、蒐集新聞

def find_news_url(stock, star_year, star_mon, star_day, end_year, end_mon, end_day):

    driver = webdriver.Chrome(executable_path=r"C:\Users\Yvonne\Desktop\wiki_parsed\chromedriver.exe")
    time_range = [star_mon,star_day,star_year,end_mon,end_day,end_year]
    url_box = []
    url = "https://www.google.com/search?q=" + str(stock) + "&source=lnt&tbs=cdr%3A1%2Ccd_min%3A" + str(time_range[0]) + "%2F" + str(time_range[1]) + "%2F" + str(time_range[2]) + "%2Ccd_max%3A" + str(time_range[3]) + "%2F"+ str(time_range[4]) + "%2F" + str(time_range[5]) + "&tbm=nws"
    print(url)
    driver.get(url)

    total_links = "//div[@class='bkWMgd']//*[@href]"
    ori_news = []
    watch_all_news = []

    for link in driver.find_elements_by_xpath(total_links):
        link_url = link.get_attribute('href')
        link_url = str(link_url)
        if 'news.google.com' in link_url:
            watch_all_news.append(link_url)
        else:
            ori_news.append(link_url)


    for i in watch_all_news:
        url_watch_news = i
        driver.get(url_watch_news)

        links_watch_news = "//div[@class='FVeGwb CVnAc']//*[@href]"

        for x in driver.find_elements_by_xpath(links_watch_news):
            link_url = x.get_attribute('href')
            link_url = str(link_url)
            ori_news.append(link_url)
    return ori_news
    

def generate_news(stock, star_year, star_mon, star_day, end_year, end_mon, end_day):

    total_url_box = find_news_url(stock, star_year, star_mon, star_day, end_year, end_mon, end_day)
    count = 0
    all_news = [] #把所有抓到的新聞丟進來

    for i in total_url_box:
        url = i
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        content = ""
        
        try:
            #印出新聞內文
            if '風傳媒' in soup.title.string :
                for x in soup.find_all('p'):
                    if i.has_attr('aid'):
                        content += x.text.strip()
            else:
                for x in soup.find_all('p'):
                    content += x.text.strip()
                                    
            #抓文章發布時間        
            for i in soup.get_text().split('\n'):
                if 'datePublished' in i:
                    time = i.split('"datePublished":')[1][2:12]
            else:
                    time = 'See published time from url'
            print(time)
                
            #若為全英文網站，表抓錯新聞，則跳過
            if content.encode( 'UTF-8' ).isalpha():
                pass
            else:
                count += 1
                theNews = News(url, soup.title.string, time, content, count)
                all_news.append(theNews)

        except:
            pass

    print("共有" + str(count) + "篇相關新聞" + "\n")
    return all_news



#part3: 新增了class:News、視窗ReadtheNews

class News():

    def __init__(self, link, title, time, content, number):
        self.link = link
        self.title = title
        self.time = time
        self.content = content
        self.number = number



class ReadtheNews(tk.Frame):


    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.createWidgets()

    def createWidgets(self):

        global all_news
        count = str(len(all_news))

        f1 = tkFont.Font(size = 12, family = "Courier New")
        f2 = tkFont.Font(size = 10, family = "Courier New")
        
        self.head = tk.Label(self, text = "共搜尋到" + count + "篇相關新聞", height = 3, width = 10, font = f1)
        self.head.grid(row = 0, column = 0, sticky = tk.NE + tk.SW)
        
        lst1 = ['前10筆','第11~20筆','第21~30筆']
        var1 = tk.StringVar()
        self.list = tk.OptionMenu(self, var1, *lst1) #製作下拉式表單
        self.list.config(height=2, width=10, font=f1)
        
        self.btnconfir = tk.Button(self, text = '確認', height=2, width=10, command = self.shownewstitle, font = f1)
        
        #self.choosenews= tk.Label(self, text = '選擇新聞' ,height=2, width=10, font=f1)
        
        self.shownews_1= tk.Label(self, relief="solid", justify="left",height=2, width=70, font=f1)
        self.shownews_2= tk.Label(self, relief="solid", justify="left",height=2, width=70, font=f1)
        self.shownews_3= tk.Label(self, relief="solid", justify="left",height=2, width=70, font=f1)
        self.shownews_4= tk.Label(self, relief="solid", justify="left",height=2, width=70, font=f1)
        self.shownews_5= tk.Label(self, relief="solid", justify="left",height=2, width=70, font=f1)
        self.shownews_6= tk.Label(self, relief="solid", justify="left",height=2, width=70, font=f1)
        self.shownews_7= tk.Label(self, relief="solid", justify="left",height=2, width=70, font=f1)
        self.shownews_8= tk.Label(self, relief="solid", justify="left",height=2, width=70, font=f1)
        self.shownews_9= tk.Label(self, relief="solid", justify="left",height=2, width=70, font=f1)
        self.shownews_10= tk.Label(self, relief="solid", justify="left",height=2, width=70, font=f1)
        
        self.btn1 = tk.Button(self, text = '點選', height=1, width=10, command = self.clickBtnNews1, font = f1)
        self.btn2 = tk.Button(self, text = '點選', height=1, width=10, command = self.clickBtnNews2, font = f1)
        self.btn3 = tk.Button(self, text = '點選', height=1, width=10, command = self.clickBtnNews3, font = f1)
        self.btn4 = tk.Button(self, text = '點選', height=1, width=10, command = self.clickBtnNews4, font = f1)
        self.btn5 = tk.Button(self, text = '點選', height=1, width=10, command = self.clickBtnNews5, font = f1)
        self.btn6 = tk.Button(self, text = '點選', height=1, width=10, command = self.clickBtnNews6, font = f1)
        self.btn7 = tk.Button(self, text = '點選', height=1, width=10, command = self.clickBtnNews7, font = f1)
        self.btn8 = tk.Button(self, text = '點選', height=1, width=10, command = self.clickBtnNews8, font = f1)
        self.btn9 = tk.Button(self, text = '點選', height=1, width=10, command = self.clickBtnNews9, font = f1)
        self.btn10 = tk.Button(self, text = '點選', height=1, width=10, command = self.clickBtnNews10, font = f1)
        
        
        self.btnconfir.grid(row = 1, column = 1)
        self.list.grid(row=1, column=0, sticky = tk.NE)
        #self.choosenews.grid(row = 1, column = 0, sticky = tk.NE)
        self.shownews_1.grid(row = 2, column = 0, sticky = tk.NE)
        self.shownews_2.grid(row = 3, column = 0, sticky = tk.NE)
        self.shownews_3.grid(row = 4, column = 0, sticky = tk.NE)
        self.shownews_4.grid(row = 5, column = 0, sticky = tk.NE)
        self.shownews_5.grid(row = 6, column = 0, sticky = tk.NE)
        self.shownews_6.grid(row = 7, column = 0, sticky = tk.NE)
        self.shownews_7.grid(row = 8, column = 0, sticky = tk.NE)
        self.shownews_8.grid(row = 9, column = 0, sticky = tk.NE)
        self.shownews_9.grid(row = 10, column = 0, sticky = tk.NE)
        self.shownews_10.grid(row = 11, column = 0, sticky = tk.NE)
        
        
        self.btn1.grid(row = 2, column = 1, sticky = tk.NE)
        self.btn2.grid(row = 3, column = 1, sticky = tk.NE)
        self.btn3.grid(row = 4, column = 1, sticky = tk.NE)
        self.btn4.grid(row = 5, column = 1, sticky = tk.NE)
        self.btn5.grid(row = 6, column = 1, sticky = tk.NE)
        self.btn6.grid(row = 7, column = 1, sticky = tk.NE)
        self.btn7.grid(row = 8, column = 1, sticky = tk.NE)
        self.btn8.grid(row = 9, column = 1, sticky = tk.NE)
        self.btn9.grid(row = 10, column = 1, sticky = tk.NE)
        self.btn10.grid(row = 11, column = 1, sticky = tk.NE)
        
        
        self.show = tk.Label(self, relief="solid", borderwidth=0.5, wraplength="1350" ,justify="left",height=17, width=140, font=f1)
        self.show.grid(row = 12)
        
    def shownewstitle(self):
        choose = self.list.cget('text')
        if choose == '前10筆':
            self.shownews_1["text"] = all_news[1].title[:40] + '...'
            self.shownews_2["text"] = all_news[2].title[:40] + '...'
            self.shownews_3["text"] = all_news[3].title[:40] + '...'
            self.shownews_4["text"] = all_news[4].title[:40] + '...'
            self.shownews_5["text"] = all_news[5].title[:40] + '...'
            self.shownews_6["text"] = all_news[6].title[:40] + '...'
            self.shownews_7["text"] = all_news[7].title[:40] + '...'
            self.shownews_8["text"] = all_news[8].title[:40] + '...'
            self.shownews_9["text"] = all_news[9].title[:40] + '...'
            self.shownews_10["text"] = all_news[10].title[:40] + '...'
        elif choose == '第11~20筆':
            self.shownews_1["text"] = all_news[11].title[:40] + '...'
            self.shownews_2["text"] = all_news[12].title[:40] + '...'
            self.shownews_3["text"] = all_news[13].title[:40] + '...'
            self.shownews_4["text"] = all_news[14].title[:40] + '...'
            self.shownews_5["text"] = all_news[15].title[:40] + '...'
            self.shownews_6["text"] = all_news[16].title[:40] + '...'
            self.shownews_7["text"] = all_news[17].title[:40] + '...'
            self.shownews_8["text"] = all_news[18].title[:40] + '...'
            self.shownews_9["text"] = all_news[19].title[:40] + '...'
            self.shownews_10["text"] = all_news[20].title[:40] + '...'
        elif choose == '第21~30筆':
            self.shownews_1["text"] = all_news[21].title[:40] + '...'
            self.shownews_2["text"] = all_news[22].title[:40] + '...'
            self.shownews_3["text"] = all_news[23].title[:40] + '...'
            self.shownews_4["text"] = all_news[24].title[:40] + '...'
            self.shownews_5["text"] = all_news[25].title[:40] + '...'
            self.shownews_6["text"] = all_news[26].title[:40] + '...'
            self.shownews_7["text"] = all_news[27].title[:40] + '...'
            self.shownews_8["text"] = all_news[28].title[:40] + '...'
            self.shownews_9["text"] = all_news[29].title[:40] + '...'
            self.shownews_10["text"] = all_news[30].title[:40] + '...'

            
    def printNews(self, article):
        self.show["text"] = article
            
    def clickBtnNews1(self):
        #showcontent = all_news[0].link + '\n' + all_news[0].content
        choose = self.list.cget('text')
        if choose == '前10筆':
            self.printNews(all_news[1].content)
        elif choose == '第11~20筆':
            self.printNews(all_news[11].content)
        elif choose == '第21~30筆':
            self.printNews(all_news[21].content)
    def clickBtnNews2(self):
        choose = self.list.cget('text')
        if choose == '前10筆':
            self.printNews(all_news[2].content)
        elif choose == '第11~20筆':
            self.printNews(all_news[12].content)
        elif choose == '第21~30筆':
            self.printNews(all_news[22].content)
    def clickBtnNews3(self):
        choose = self.list.cget('text')
        if choose == '前10筆':
            self.printNews(all_news[3].content)
        elif choose == '第11~20筆':
            self.printNews(all_news[13].content)
        elif choose == '第21~30筆':
            self.printNews(all_news[23].content)
    def clickBtnNews4(self):
        choose = self.list.cget('text')
        if choose == '前10筆':
            self.printNews(all_news[4].content)
        elif choose == '第11~20筆':
            self.printNews(all_news[14].content)
        elif choose == '第21~30筆':
            self.printNews(all_news[24].content)
    def clickBtnNews5(self):
        choose = self.list.cget('text')
        if choose == '前10筆':
            self.printNews(all_news[5].content)
        elif choose == '第11~20筆':
            self.printNews(all_news[15].content)
        elif choose == '第21~30筆':
            self.printNews(all_news[25].content)
    def clickBtnNews6(self):
        choose = self.list.cget('text')
        #showcontent = all_news[0].link + '\n' + all_news[0].content
        if choose == '前10筆':
            self.printNews(all_news[6].content)
        elif choose == '第11~20筆':
            self.printNews(all_news[16].content)
        elif choose == '第21~30筆':
            self.printNews(all_news[26].content)    
    def clickBtnNews7(self):
        choose = self.list.cget('text')
        if choose == '前10筆':
            self.printNews(all_news[7].content)
        elif choose == '第11~20筆':
            self.printNews(all_news[17].content)
        elif choose == '第21~30筆':
            self.printNews(all_news[27].content)
    def clickBtnNews8(self):
        choose = self.list.cget('text')
        if choose == '前10筆':
            self.printNews(all_news[8].content)
        elif choose == '第11~20筆':
            self.printNews(all_news[18].content)
        elif choose == '第21~30筆':
            self.printNews(all_news[28].content)
    def clickBtnNews9(self):
        choose = self.list.cget('text')
        if choose == '前10筆':
            self.printNews(all_news[9].content)
        elif choose == '第11~20筆':
            self.printNews(all_news[19].content)
        elif choose == '第21~30筆':
            self.printNews(all_news[29].content)
    def clickBtnNews10(self):
        choose = self.list.cget('text')
        if choose == '前10筆':
            self.printNews(all_news[10].content)
        elif choose == '第11~20筆':
            self.printNews(all_news[20].content)
        elif choose == '第21~30筆':
            self.printNews(all_news[30].content)
        
        



# In[46]:

stockid = input('')
time_start = input('').split('/') #ex:2018/3/27
time_end = input('').split('/')
all_news = generate_news(stockid, time_start[0], time_start[1], time_start[2], time_end[0], time_end[1], time_end[2])

read = ReadtheNews()
read.master.title("我要看新聞")
read.mainloop()


