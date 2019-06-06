def crawl_finance(stock_id):
    import requests
    import datetime
    import pandas as pd
    import matplotlib.pyplot as plt
    now = int(datetime.datetime.now().timestamp())+86400
    url = "https://query1.finance.yahoo.com/v7/finance/download/" + stock_id + "?period1=0&period2=" + str(now) + "&interval=1d&events=history&crumb=hP2rOschxO0"
    response = requests.post(url)

    with open("stockfile.csv", "w") as f:
        f.writelines(response.text)
    
    import pandas as pd
    fine_stockdata = pd.read_csv("stockfile.csv", index_col = "Date", parse_dates = ["Date"])

def draw_figure(begin_year,last_year):
    import pandas as pd
    yearlist = []
    for i in range( int(last_year) - int(begin_year) + 1 ):
        yearlist.append(str(int(begin_year)+i))
    
    import csv
    list_ = []
    with open("stockfile.csv", "r") as f:
        tite = f.readline()
        a = csv.reader( f )
        for aline in a:
            if aline[0][:4] in yearlist:
                list_.append( aline )

    with open("chose_period.csv","w") as c:
        c.write(tite)
        for element in list_:
            for i in range(len(element)):
                if i == len(element) - 1:
                    c.write(element[i])
                else:
                    c.write(element[i]+",")     
            c.write("\n")

    with open("chose_period.csv","r") as d:
        e = pd.read_csv("chose_period.csv", index_col = "Date", parse_dates = ["Date"])
        import matplotlib.pyplot as plt
        e.Close.plot()
        plt.show()
        


stock_id = input()
wanted_period = input()
begin_year = wanted_period.split(",")[0]
last_year = wanted_period.split(",")[1]
crawl_finance(stock_id)
draw_figure(begin_year,last_year)