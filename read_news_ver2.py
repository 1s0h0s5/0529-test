
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

    driver = webdriver.Chrome(executable_path=r"D:\\PBC_Spring_2019\\chromedriver.exe")
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
        count += 1
        content = ""
        
        try:
            if '風傳媒' in soup.title.string :
                for x in soup.find_all('p'):
                    if i.has_attr('aid'):
                        content += x.text.strip()
            else:
                for x in soup.find_all('p'):
                    content += x.text.strip()
                         #連結       標題           內文    第幾篇
            theNews = News(url, soup.title.string, content, count)
            all_news.append(theNews)

        except:
            pass

    print("共有" + str(count) + "篇相關新聞" + "\n")
    return all_news



#part3: 新增了class:News、視窗ReadtheNews

class News():

    def __init__(self, link, title, content, number):
        self.link = link
        self.title = title
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

        self.btnNews1 = tk.Button(self, text = all_news[0].title[:15] + "...", height=2, width=50, command = self.clickBtnNews1, font = f1)
        self.btnNews2 = tk.Button(self, text = all_news[1].title[:15] + "...", height=2, width=50, command = self.clickBtnNews2, font = f1)
        self.btnNews3 = tk.Button(self, text = all_news[2].title[:15] + "...", height=2, width=50, command = self.clickBtnNews3, font = f1)
        self.btnNews4 = tk.Button(self, text = all_news[3].title[:15] + "...", height=2, width=50, command = self.clickBtnNews4, font = f1)
        self.btnNews5 = tk.Button(self, text = all_news[4].title[:15] + "...", height=2, width=50, command = self.clickBtnNews5, font = f1)

        self.btnNews1.grid(row = 1, column = 0, sticky = tk.NE + tk.SW)
        self.btnNews2.grid(row = 2, column = 0, sticky = tk.NE + tk.SW)
        self.btnNews3.grid(row = 3, column = 0, sticky = tk.NE + tk.SW)
        self.btnNews4.grid(row = 4, column = 0, sticky = tk.NE + tk.SW)
        self.btnNews5.grid(row = 5, column = 0, sticky = tk.NE + tk.SW)

        #顯示新聞內文
        self.show = tk.Label(self, text = "點選任一標題", height=30, width=50, font=f2)
        self.show.grid(row = 6, column = 0, sticky = tk.NE + tk.SW)

    def printNews(self, title, link, content):
        article = "新聞標題: " + title + "\n"
        article+= "原文網址: " + link + "\n"
        article+= "新聞內容: " + content
        
        self.show.config(text = article) 

    def clickBtnNews1(self):
        self.printNews(all_news[0].title, all_news[0].link, all_news[0].content)
    def clickBtnNews2(self):
        self.printNews(all_news[1].title, all_news[1].link, all_news[1].content)
    def clickBtnNews3(self):
        self.printNews(all_news[2].title, all_news[2].link, all_news[2].content)
    def clickBtnNews4(self):
        self.printNews(all_news[3].title, all_news[3].link, all_news[3].content)
    def clickBtnNews5(self):
        self.printNews(all_news[4].title, all_news[4].link, all_news[4].content)




# In[46]:

all_news = generate_news(2330, 2018, 3, 1, 2018, 3, 10)

read = ReadtheNews()
read.master.title("我要看新聞")
read.mainloop()


"""
for news in all_news:
    print("第"+str(news.number)+"篇")
    print("連結: ", news.link)
    print("標題: ", news.title)
    print("內文: \n", news.content.strip(), "\n")

    if news.number == 10:
        break


台積電2330，鴻海2317，聯發科2454，中華電信2412，統一1216，大立光3008
"""