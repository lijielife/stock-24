import sys
import os
from stock import Stock
from datetime import date, datetime, timedelta
from indicator import *

stocks = {}  #Key is tiker, value is Stock object

def load_stocks(folder, days):
    infos = []
    for root, dirs, files in os.walk(folder):
        for f in files:
            infos.append(f)
    infos.sort()
    for fname in infos[-days:]:
        f = open(folder + fname, 'r')
        count = 0
        for line in f:
            count += 1
            if count == 1: continue
            data = line.split(',')
            ticker = data[0]
            if ticker not in stocks:
                stocks[ticker] = Stock(ticker)
            d = data[1]
            day = date(int(d[:4]), int(d[4:6]), int(d[6:]))
            stocks[ticker].add_data(day, data[2],
                   data[3], data[4], data[5], data[6])

    


def analyze():
    output = open(str(datetime.now().date()), 'w')
    for key in stocks:
        stock = stocks[key]
        for i in range(14,16):
            day = (datetime.now() - timedelta(days=i)).date()
            day_before = (datetime.now() - timedelta(days=i+1)).date()         
            today_10 = EMA_Stock(stock, 10, day)
            today_20 = EMA_Stock(stock, 20, day)
            yesterday_10 = EMA_Stock(stock, 10, day_before)
            yesterday_20 = EMA_Stock(stock, 20, day_before
            if yesterday_10 < yesterday_20 and today_10 >= today_20:
                output.write(stock.ticker + ',' + str(day))

    output.close()


        


if __name__ == '__main__':
    folder = sys.argv[1]
    days = int(sys.argv[2])
    load_stocks(folder, days)
    #print stocks['AAPL'].repr_one_day(0)
    analyze()
        
    
