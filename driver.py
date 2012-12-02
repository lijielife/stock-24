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
        try:
            stock = stocks[key]
            for i in range(1, 3):
                day = (datetime.now() - timedelta(days=i)).date()
                day_before = (datetime.now() - timedelta(days=i+1)).date()   
                today_10 = EMA_Stock(stock, 10, day)
                today_20 = EMA_Stock(stock, 20, day)
                yesterday_10 = EMA_Stock(stock, 10, day_before)
                yesterday_20 = EMA_Stock(stock, 20, day_before)
                if yesterday_10 < yesterday_20 and today_10 >= today_20:
                    tempIndex = stock.get_index_of_date( day )
                    output.write( str( tempIndex ) + ", " + str( stock.closes[ tempIndex ] ) + " ::: " )
                    output.write(stock.ticker + ',' + str(day) + "  :::  " + str( yesterday_10 ) + ", " + str( yesterday_20 ) + ", " + str( today_10 ) + ", " + str( today_20 ) + ", " + '\n')
        except:
            print key + ": not enough data for analyzing"
    output.close()


        


if __name__ == '__main__':
    folder = sys.argv[1]
    days = int(sys.argv[2])
    load_stocks(folder, days)
    #print stocks['AAPL'].repr_one_day(0)
    analyze()
        
    
