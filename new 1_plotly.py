import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os


def crawl_finance(stock_id):
	now = int(datetime.datetime.now().timestamp())+86400
	url = "https://query1.finance.yahoo.com/v7/finance/download/" + stock_id + "?period1=0&period2=" + str(now) + "&interval=1d&events=history&crumb=hP2rOschxO0"
	response = requests.post(url)

	with open( "C:\\Users\\anan2\\Desktop\\stockfile.csv", "w") as f:
		f.writelines(response.text)

	fine_stockdata = pd.read_csv("C:\\Users\\anan2\\Desktop\\stockfile.csv", index_col = "Date", parse_dates = ["Date"])

def draw_figure(begin_year,last_year):
	yearlist = []
	for i in range( int(last_year) - int(begin_year) + 1 ):
		yearlist.append(str(int(begin_year)+i))
	
	list_ = []
	year_ = []
	close_ = []
	with open("C:\\Users\\anan2\\Desktop\\stockfile.csv", "r") as f:
		tite = f.readline()
		a = csv.reader( f )
		for aline in a:
			if aline[0][:4] in yearlist and aline[1] != 'null': #不選擇沒有資料的日期
				year_.append(aline[0][:4])
				close_.append(aline[4])
				list_.append( aline )

	with open("C:\\Users\\anan2\\Desktop\\chose_period.csv","w") as c:
		c.write(tite)
		for element in list_:
			for i in range(len(element)):
				if i == len(element) - 1:
					c.write(element[i])
				else:
					c.write(element[i]+",")	 
			c.write("\n")
	#show the interactive graph
	import plotly 
	plotly.tools.set_credentials_file(username='yvonnemin', api_key='0OB0RQFVhOE3lVt1Y5R7') #sign in ID, API Key to use the function

	import plotly.plotly as py
	import plotly.graph_objs as go

	#Loading stock price(y) and time series(x)
	trace = go.Scatter(
		x = year_,
		y = close_,
		mode = 'lines'
	)

	data = [trace] #Can draw more than one data series
	py.plot(data, filename='scatter-mode')			
			
#	with open("C:\\Users\\anan2\\Desktop\\chose_period.csv","r") as d:
#		e = pd.read_csv("C:\\Users\\anan2\\Desktop\\chose_period.csv", index_col = "Date", parse_dates = ["Date"])
#		e.Close.plot()
#		plt.show()


#stock_id = input()
stock_id = '2330'
#wanted_period = input()
wanted_period = "2015,2017"
begin_year = wanted_period.split(",")[0]
last_year = wanted_period.split(",")[1]
crawl_finance(stock_id)
draw_figure(begin_year,last_year)