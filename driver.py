import sys
import os
from stock import Stock
from datetime import date, datetime, timedelta
from indicator import *

stocks = {}  #Key is ticker, value is Stock object

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
    output = open(str(datetime.now().date())+'.txt', 'w')
    for key in stocks:
        try:
            stock = stocks[key]
            for i in range(0, 5):
                day = (datetime.now() - timedelta(days=i)).date()
                dayIndex = stock.get_index_of_date( day )
                    
                # check EMA rule
                day_before = dayIndex - 1 #(datetime.now() - timedelta(days=i+1)).date()   
                today_5 = EMA_Stock(stock, 5, dayIndex)
                today_10 = EMA_Stock(stock, 10, dayIndex)
                today_50 = EMA_Stock(stock, 50, dayIndex)
                yesterday_5 = EMA_Stock(stock, 5, day_before)
                yesterday_10 = EMA_Stock(stock, 10, day_before)
                yesterday_50 = EMA_Stock(stock, 50, day_before)
                is_ema_good = check_ema( ( today_5, today_10, today_50 ), ( yesterday_5, yesterday_10, yesterday_50 ) , stock, dayIndex)

                # check ForceIndex rule
                force_index_2 = ForceIndex( stock, 2, dayIndex )
                force_index_13 = ForceIndex( stock, 13, dayIndex )
                is_force_index_good = check_force_index( ( force_index_2, force_index_13 ) )

                # check Bollinger rule
                bollinger_band = BollingBand_Stock( stock, 20, dayIndex )
                is_bollinger_good = check_bollinger( bollinger_band, stock.closes[ dayIndex ] )

                # check price rule
                is_price_good = check_price( stock.closes[ dayIndex ] )

                # check volume rule
                is_volume_good = check_volumes( stock, day, dayIndex )
                is_volume2_good = check_volumes2( stock.volumes[ dayIndex ] )

                # check Stochastic rule
                is_stochastic_good = check_stochastic( stock, 14, 3, 3, dayIndex )

                # is_ema_good = True
                # is_force_index_good = True
                # is_bollinger_good = True
                # is_price_good = True
                #is_volume_good = True
                #is_volume2_good = True
                #is_stochastic_good = True

                if is_ema_good and is_force_index_good and is_bollinger_good and is_price_good and is_volume_good and is_volume2_good and is_stochastic_good:
                    highest_close_after = max( stock.closes[ dayIndex : dayIndex + 5] )
                    highest_high_after = max( stock.highs[ dayIndex : dayIndex + 5] )
                    output.write( str( highest_close_after / stock.closes[ dayIndex ] ) + ", " + str( highest_high_after /  stock.closes[ dayIndex ] ) + " ::: " )      # print the earning ratio
                    output.write(stock.ticker + ',' + str(day) + '\n')
                    print stock.ticker + ',' + str(day)
        except:
            print key + ": not enough data for analyzing"
    print 'finish';
    output.write('finish' + '\n')
    output.close() 

def check_ema( now_emas, before_emas , stock, dayIndex):
    #return before_emas[ 0 ] < before_emas[ 1 ] and now_emas[ 0 ] >= now_emas[ 1 ] and now_emas[ 0 ] < now_emas[ 2 ] and now_emas[ 1 ] < now_emas[ 2 ] 
    return now_emas[ 0 ] > before_emas[ 0 ] and now_emas[ 1 ] > before_emas[ 1 ] and now_emas[ 0 ] >= now_emas[ 2 ] and now_emas[ 1 ] >= now_emas[ 2 ] and stock.highs[ dayIndex ] >= now_emas[ 0 ]

def check_force_index( force_index_tuple ):
    return force_index_tuple[ 0 ] > 0 and force_index_tuple[ 1 ] > 0
    #return force_index_tuple[ 1 ] > 0

def check_bollinger( bollinger_band, close ):
    #return close < bollinger_band[ 1 ] and (bollinger_band[ 2 ] - bollinger_band[ 0 ]) >= 0.5
    return (bollinger_band[ 2 ] - bollinger_band[ 0 ]) >= 0.5

def check_price( close ):
    return close > 1

def check_volumes( stock, day, dayIndex ):
    recent_max_volume = max( stock.volumes[ dayIndex - 2 : dayIndex ] )
    return recent_max_volume > 1.5 * Average_Volume( stock, 50, dayIndex )

def check_stochastic( stock, k_min_max_length, k_smooth_length, d_length, dayIndex ):
    pair = Stochastic_Stock( stock, k_min_max_length, k_smooth_length, d_length, dayIndex )
    return pair[ 0 ] <= 50

def check_volumes2( volume ):
    return volume > 10000

if __name__ == '__main__':
    folder = sys.argv[1]
    days = int(sys.argv[2])
    load_stocks(folder, days)
    #print stocks['AAPL'].repr_one_day(0)
    analyze()
        
    
