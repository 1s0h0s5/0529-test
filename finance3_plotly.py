def crawl_finance(stock_id):
	import requests
	import datetime
	now = int(datetime.datetime.now().timestamp())+86400
	url = "https://query1.finance.yahoo.com/v7/finance/download/" + stock_id + "?period1=0&period2=" + str(now) + "&interval=1d&events=history&crumb=hP2rOschxO0"
	response = requests.post(url)

	with open("C:\\Users\\anan2\\Desktop\\stockfile.csv", "w") as f:
		f.writelines(response.text)
	import pandas as pd
	fine_stockdata = pd.read_csv("C:\\Users\\anan2\\Desktop\\stockfile.csv", index_col = "Date", parse_dates = ["Date"])

def draw_figure(begin_year,last_year):
	#將選擇時段列成一個年份清單yearlist
	yearlist = []
	for i in range( int(last_year) - int(begin_year) + 1 ):
		yearlist.append(str(int(begin_year)+i))
	
	#將選定時段內的資料存到清單中，且略去沒有紀錄的日期資料
	import csv
	temporary_list_ = []
	with open("C:\\Users\\anan2\\Desktop\\stockfile.csv", "r") as f:
		title = f.readline()
		a = csv.reader( f )
		for aline in a:
			if aline[0][:4] in yearlist and aline[1] != 'null': #不選擇沒有資料的日期
				temporary_list_.append( aline )
	
	#前一個statement將所存下的資料放到CSV中，以便後面製作互動式圖表
	with open("C:\\Users\\anan2\\Desktop\\chose_period.csv","w") as c:
		c.write(title)
		for element in temporary_list_:
			for i in range(len(element)):
				if i == len(element) - 1:
					c.write(element[i])
				else:
					c.write(element[i]+",")	 
			c.write("\n")
			
	#製作互動式圖表，到時候的圖片可以透過放大來顯示更細的時間區段
	import pandas as pd
	file = 'C:\\Users\\anan2\\Desktop\\chose_period.csv'
	pd = pd.read_csv(file)
	y_values = pd['Close']
	x_values = pd['Date']
	x_list=[]
	y_list=[]
	for j in y_values:
		y_list.append(j)
	for i in x_values:
		x_list.append(i)
	

	#sign in ID, API Key to use the function
	import plotly
	plotly.tools.set_credentials_file(username='yvonnemin', api_key='0OB0RQFVhOE3lVt1Y5R7') 

	#Loading stock price(y) and time series(x)
	import plotly.plotly as py
	import plotly.graph_objs as go
	trace = go.Scatter(
		x = x_list,
		y = y_list,
		mode = 'lines'
	)
	
	data = [trace]	#Can draw more than one data series
	py.plot(data, filename='scatter-mode')	  

#stock_id = input()
stock_id = '2002'
#wanted_period = input()
wanted_period = '2000,2018'
begin_year = wanted_period.split(",")[0]
last_year = wanted_period.split(",")[1]
crawl_finance(stock_id)
draw_figure(begin_year,last_year)