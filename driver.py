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
            for i in range(15, 30):
                day = (datetime.now() - timedelta(days=i)).date()
                dayIndex = stock.get_index_of_date( day )
                    
                # check EMA rule
                day_before = (datetime.now() - timedelta(days=i+1)).date()   
                today_5 = EMA_Stock(stock, 10, day)
                today_10 = EMA_Stock(stock, 20, day)
                today_50 = EMA_Stock(stock, 50, day)
                yesterday_5 = EMA_Stock(stock, 10, day_before)
                yesterday_10 = EMA_Stock(stock, 20, day_before)
                yesterday_50 = EMA_Stock(stock, 50, day_before)
                is_ema_good = check_ema( ( today_5, today_10, today_50 ), ( yesterday_5, yesterday_10, yesterday_50 ) )
                print 1

                # check ForceIndex rule
                force_index_2 = ForceIndex( stock, 2, day )
                print 1.3
                force_index_13 = ForceIndex( stock, 13, day )
                print 1.5
                is_force_index_good = check_force_index( ( force_index_2, force_index_13 ) )
                print 2

                # check Bollinger rule
                bollinger_band = BollingBand_Stock( stock, 20, day )
                print 2.5
                is_bollinger_good = check_bollinger( bollinger_band, stock.closes[ dayIndex ] )
                print 3

                # check price rule
                is_price_good = check_price( stock.closes[ dayIndex ] )
                print 4

                # check volume rule
                is_volume_good = check_volumes( stock, day, dayIndex )
                print 5

                # check Stochastic rule

                # is_ema_good = True
                # is_force_index_good = True
                # is_bollinger_good = True
                # is_price_good = True
                # is_volume_good = True

                if is_ema_good and is_force_index_good and is_bollinger_good and is_price_good and is_volume_good:
                    print 6
                    highest_close_after = max( stock.closes[ dayIndex + 2 : dayIndex + 10 ] )
                    print 7
                    highest_high_after = max( stock.highs[ dayIndex + 2 : dayIndex + 10 ] )
                    print 8
                    output.write( str( highest_close_after / stock.closes[ dayIndex ] ) + ", " + str( highest_high_after /  stock.closes[ dayIndex ] ) + " ::: " )      # print the earning ratio
                    output.write(stock.ticker + ',' + str(day) + '\n')
                    print 9
        except:
            print key + ": not enough data for analyzing"
    output.close() 

def check_ema( now_emas, before_emas ):
    return before_emas[ 0 ] <= before_emas[ 1 ] and now_emas[ 0 ] > now_emas[ 1 ] #and now_emas[ 0 ] < now_emas[ 2 ] and now_emas[ 1 ] < now_emas[ 2 ] 

def check_force_index( force_index_tuple ):
    for force_index in force_index_tuple:
        if force_index < 0 :
            return False
    return True

def check_bollinger( bollinger_band, close ):
    return close < bollinger_band[ 1 ]

def check_price( close ):
    return close > 1

def check_volumes( stock, day, dayIndex ):
    recent_max_volume = max( stock.volumes[ dayIndex - 2 : dayIndex ] )
    return recent_max_volume > 1.5 * Average_Volume( stock, 50, day )

if __name__ == '__main__':
    folder = sys.argv[1]
    days = int(sys.argv[2])
    load_stocks(folder, days)
    #print stocks['AAPL'].repr_one_day(0)
    analyze()
        
    
