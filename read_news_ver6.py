
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
from tkinter import ttk



#part3: 新增了class:News、視窗ReadtheNews

class News():

    def __init__(self, link, title, time, content, number):
        self.link = link
        self.title = title
        self.time = time
        self.content = content
        self.number = number


class ReadTheNews(tk.Frame):
    all_news = []

    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.createWidgets()

    def createWidgets(self):

        global all_news
        count = str(len(all_news))

        f1 = tkFont.Font(size = 12, family = "Courier New")
        f2 = tkFont.Font(size = 16, family = "Berlin Sans FB Demi")
        
        #使用者輸入變數
        self.head = tk.Label(self, text = "股價新聞小幫手", height = 2, width = 20, font = f2) #執行完的text會變成 "共搜尋到" + count + "篇相關新聞"
        self.askforid = tk.Label(self, text = "請輸入股價代碼:", height = 1, width = 15, font = f1)
        self.idInput = tk.Text(self, height = 1, width = 5, font = f1)

        self.askfortime = tk.Label(self, text = "請輸入時間範圍(格式:2019/6/17)", height = 1, width = 25, font = 1)
        self.startInput = tk.Text(self, height = 1, width = 5, font = f1)
        self.endInput = tk.Text(self, height = 1, width = 5, font = f1)
        self.run = tk.Button(self, text = "執行", height=1, width=5, command = self.run, font = f1)

        self.head.grid(row = 0, column = 0, columnspan = 6, sticky = tk.NE + tk.SW)
        self.askforid.grid(row = 1, column = 0, sticky = tk.NE + tk.SW)
        self.idInput.grid(row = 1, column = 1, sticky = tk.NE + tk.SW)
        self.askfortime.grid(row = 1, column = 2, sticky = tk.NE + tk.SW)
        self.startInput.grid(row = 1, column = 3, sticky = tk.NE + tk.SW)
        self.endInput.grid(row = 1, column = 4, sticky = tk.NE + tk.SW)
        self.run.grid(row = 1, column = 5, sticky = tk.NW)


        #製作下拉式表單，選擇第__筆~第__筆新聞
        lst1 = ['第1~5筆', '第6~10筆', '第11~15筆', '第16~20筆', '第21~25筆', '第26~30筆']
        var1 = tk.StringVar()
        self.list = tk.OptionMenu(self, var1, *lst1)
        self.list.config(height=1, width=10, font=f1)
        self.btnconfir = tk.Button(self, text = '確認', height=1, width=5, command = self.shownewstitle, font = f1)

        
        #右邊的標題列&選擇要讀哪一篇
        self.shownews_1= tk.Label(self, relief="solid", justify="left",height=2, width=60, font=f1)
        self.shownews_2= tk.Label(self, relief="solid", justify="left",height=2, width=60, font=f1)
        self.shownews_3= tk.Label(self, relief="solid", justify="left",height=2, width=60, font=f1)
        self.shownews_4= tk.Label(self, relief="solid", justify="left",height=2, width=60, font=f1)
        self.shownews_5= tk.Label(self, relief="solid", justify="left",height=2, width=60, font=f1)

        self.btn1 = tk.Button(self, text = '點選', height=1, width=5, command = self.clickBtnNews1, font = f1)
        self.btn2 = tk.Button(self, text = '點選', height=1, width=5, command = self.clickBtnNews2, font = f1)
        self.btn3 = tk.Button(self, text = '點選', height=1, width=5, command = self.clickBtnNews3, font = f1)
        self.btn4 = tk.Button(self, text = '點選', height=1, width=5, command = self.clickBtnNews4, font = f1)
        self.btn5 = tk.Button(self, text = '點選', height=1, width=5, command = self.clickBtnNews5, font = f1)


        self.btnconfir.grid(row = 2, column = 4, sticky = tk.NW)
        self.list.grid(row=2, column=3, sticky = tk.NE)

        self.shownews_1.grid(row = 3, column = 3, columnspan = 2, sticky = tk.NE)
        self.shownews_2.grid(row = 4, column = 3, columnspan = 2, sticky = tk.NE)
        self.shownews_3.grid(row = 5, column = 3, columnspan = 2, sticky = tk.NE)
        self.shownews_4.grid(row = 6, column = 3, columnspan = 2, sticky = tk.NE)
        self.shownews_5.grid(row = 7, column = 3, columnspan = 2, sticky = tk.NE)

        self.btn1.grid(row = 3, column = 5, sticky = tk.NW)
        self.btn2.grid(row = 4, column = 5, sticky = tk.NW)
        self.btn3.grid(row = 5, column = 5, sticky = tk.NW)
        self.btn4.grid(row = 6, column = 5, sticky = tk.NW)
        self.btn5.grid(row = 7, column = 5, sticky = tk.NW)


        #在最底下顯示全文內容
        self.show = tk.Message(self, text="", anchor=tk.NW, justify="left", width=1200, padx=3, pady=2, font=f1)
        self.show.grid(row = 13, column = 0, columnspan = 6, sticky = tk.NW)



    ### {[執行!!]}
    def run(self):
        stockid = self.idInput.get("1.0", 'end-1c')
        time_start = self.startInput.get("1.0", 'end-1c').split('/') #ex:2018/3/27
        time_end = self.endInput.get("1.0", 'end-1c').split('/')

        #搜尋、抓網頁
        def find_news_url(stock, star_year, star_mon, star_day, end_year, end_mon, end_day):

            driver = webdriver.Chrome(executable_path=r"D:\\PBC_Spring_2019\\chromedriver.exe") 
            #要跑的電腦都要下載chromedriver，然後改成自己的路徑!!
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

        #爬蟲、蒐集新聞
        def generate_news(stock, star_year, star_mon, star_day, end_year, end_mon, end_day):

            total_url_box = find_news_url(stock, star_year, star_mon, star_day, end_year, end_mon, end_day)
            count = 0
            global all_news
            t_set = set()

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

                    title = soup.title.string.strip()
                    #若為全英文網站，表抓錯新聞，則跳過
                    if title.encode( 'UTF-8' ).isalpha():
                        pass
                    else:
                        count += 1
                        theNews = News(url, title, time, content, count)
                        if title not in t_set:
                            all_news.append(theNews)
                            t_set.add(title)
                except:
                    pass

            return all_news
            
        all_news = generate_news(stockid, time_start[0], time_start[1], time_start[2], time_end[0], time_end[1], time_end[2])
        self.head["text"] = "完成! 共找到" + str(len(all_news)) + "篇新聞!"
        return all_news


    def shownewstitle(self):
        choose = self.list.cget('text')
        if choose == '第1~5筆':
            self.shownews_1["text"] = all_news[1].title[:30] + '...'
            self.shownews_2["text"] = all_news[2].title[:30] + '...'
            self.shownews_3["text"] = all_news[3].title[:30] + '...'
            self.shownews_4["text"] = all_news[4].title[:30] + '...'
            self.shownews_5["text"] = all_news[5].title[:30] + '...'

        elif choose == '第6~10筆':
            self.shownews_1["text"] = all_news[6].title[:30] + '...'
            self.shownews_2["text"] = all_news[7].title[:30] + '...'
            self.shownews_3["text"] = all_news[8].title[:30] + '...'
            self.shownews_4["text"] = all_news[9].title[:30] + '...'
            self.shownews_5["text"] = all_news[10].title[:30] + '...'

        elif choose == '第11~15筆':
            self.shownews_1["text"] = all_news[11].title[:30] + '...'
            self.shownews_2["text"] = all_news[12].title[:30] + '...'
            self.shownews_3["text"] = all_news[13].title[:30] + '...'
            self.shownews_4["text"] = all_news[14].title[:30] + '...'
            self.shownews_5["text"] = all_news[15].title[:30] + '...'

        elif choose == '第16~20筆':
            self.shownews_1["text"] = all_news[16].title[:30] + '...'
            self.shownews_2["text"] = all_news[17].title[:30] + '...'
            self.shownews_3["text"] = all_news[18].title[:30] + '...'
            self.shownews_4["text"] = all_news[19].title[:30] + '...'
            self.shownews_5["text"] = all_news[20].title[:30] + '...'

        elif choose == '第21~25筆':
            self.shownews_1["text"] = all_news[21].title[:30] + '...'
            self.shownews_2["text"] = all_news[22].title[:30] + '...'
            self.shownews_3["text"] = all_news[23].title[:30] + '...'
            self.shownews_4["text"] = all_news[24].title[:30] + '...'
            self.shownews_5["text"] = all_news[25].title[:30] + '...'

        elif choose == '第26~30筆':
            self.shownews_1["text"] = all_news[26].title[:30] + '...'
            self.shownews_2["text"] = all_news[27].title[:30] + '...'
            self.shownews_3["text"] = all_news[28].title[:30] + '...'
            self.shownews_4["text"] = all_news[29].title[:30] + '...'
            self.shownews_5["text"] = all_news[30].title[:30] + '...'

    #跑出全部文章內容
    def printNews(self, theNews):
        article = "新聞標題: " + theNews.title + "\n"
        #article = "發佈時間: " + theNews.time + "\n" #目前還是沒有抓到正確的時間，全部都會跑出'See published time from url'
        article+= "原文網址: " + theNews.link + "\n\n"
        article+= "" + theNews.content
        self.show["text"] = article
            
    def clickBtnNews1(self):
        choose = self.list.cget('text')
        if choose == '第1~5筆':
            self.printNews(all_news[1])
        elif choose == '第6~10筆':
            self.printNews(all_news[6])
        elif choose == '第11~15筆':
            self.printNews(all_news[11])
        elif choose == '第16~20筆':
            self.printNews(all_news[16])
        elif choose == '第21~25筆':
            self.printNews(all_news[21])
        elif choose == '第26~30筆':
            self.printNews(all_news[26])

    def clickBtnNews2(self):
        choose = self.list.cget('text')
        if choose == '第1~5筆':
            self.printNews(all_news[2])
        elif choose == '第6~10筆':
            self.printNews(all_news[7])
        elif choose == '第11~15筆':
            self.printNews(all_news[12])
        elif choose == '第16~20筆':
            self.printNews(all_news[17])
        elif choose == '第21~25筆':
            self.printNews(all_news[22])
        elif choose == '第26~30筆':
            self.printNews(all_news[27])

    def clickBtnNews3(self):
        choose = self.list.cget('text')
        if choose == '第1~5筆':
            self.printNews(all_news[3])
        elif choose == '第6~10筆':
            self.printNews(all_news[8])
        elif choose == '第11~15筆':
            self.printNews(all_news[13])
        elif choose == '第16~20筆':
            self.printNews(all_news[18])
        elif choose == '第21~25筆':
            self.printNews(all_news[23])
        elif choose == '第26~30筆':
            self.printNews(all_news[28])

    def clickBtnNews4(self):
        choose = self.list.cget('text')
        if choose == '第1~5筆':
            self.printNews(all_news[4])
        elif choose == '第6~10筆':
            self.printNews(all_news[9])
        elif choose == '第11~15筆':
            self.printNews(all_news[14])
        elif choose == '第16~20筆':
            self.printNews(all_news[19])
        elif choose == '第21~25筆':
            self.printNews(all_news[24])
        elif choose == '第26~30筆':
            self.printNews(all_news[29])

    def clickBtnNews5(self):
        choose = self.list.cget('text')
        if choose == '第1~5筆':
            self.printNews(all_news[5])
        elif choose == '第6~10筆':
            self.printNews(all_news[10])
        elif choose == '第11~15筆':
            self.printNews(all_news[15])
        elif choose == '第16~20筆':
            self.printNews(all_news[20])
        elif choose == '第21~25筆':
            self.printNews(all_news[25])
        elif choose == '第26~30筆':
            self.printNews(all_news[30])





#程式開始

all_news = []
read = ReadTheNews()
read.master.title("股價新聞小幫手")
read.mainloop()