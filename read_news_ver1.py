#!/usr/bin/env python
# coding: utf-8

# In[1]:
#我自己有需要先pip install的套件：selenium, xlrd, config, bs4, beautifulsoup4
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


# In[19]:
def find_news_url(stock, star_year, star_mon, star_day, end_year, end_mon, end_day):

    #先去下載"chromedriver"，隨便放一個找得到路徑路徑的地方
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
    

# In[45]:
def generate_news(stock, star_year, star_mon, star_day, end_year, end_mon, end_day):

    total_url_box = find_news_url(stock, star_year, star_mon, star_day, end_year, end_mon, end_day)
    count = 0
    all_news = []

    for i in total_url_box:
        url = i
        count += 1
        content = ""
        # print("第"+str(count)+"則相關新聞")
        # print("原文網址:", url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        try:
            #print("新聞標題:", soup.title.string)
            # print("內文:")
            if '風傳媒' in soup.title.string :
                for x in soup.find_all('p'):
                    if i.has_attr('aid'):
                        content += x.text + "\n"
                        #print(x.text)
            else:
                for x in soup.find_all('p'):
                    content += x.text + "\n"
                    #print(x.text)

            theNews = News(url, soup.title.string, content, count)
            all_news.append(theNews)

        except:
            pass

    print("共有" + str(count) + "篇相關新聞\n")
    return all_news



#News
class News():

    def __init__(self, link, title, content, number):
        self.link = link
        self.title = title
        self.content = content
        self.number = number


#PrintNews
class ReadtheNews(tk.Frame):


    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.createWidgets()
        
    def createWidgets(self):
        f1 = tkFont.Font(size = 18, family = "Courier New")
        f2 = tkFont.Font(size = 12, family = "Courier New")




# In[46]:

all_news = generate_news(2330, 2018, 3, 1, 2018, 3, 10)




"""
for news in all_news:
    print("第"+str(news.number)+"篇")
    print("連結: ", news.link)
    print("標題: ", news.title)
    print("內文: \n", news.content)
    print()

    if news.number == 10:
        break



台積電2330，鴻海2317，聯發科2454，中華電信2412，統一1216，大立光3008
"""