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
    lost = 0
    win = 0
    win_count = 0
    lost_count = 0
    total_count = 0
                
    for key in stocks:
        try:
            stock = stocks[key]
            today = datetime.now().date()
            todayIndex = stock.get_index_of_date( today )
                
            for i in range(0, 5):
                #print 1
                dayIndex = todayIndex - i    
                #print 2
                # check EMA rule
                day_before = dayIndex - 1 #(datetime.now() - timedelta(days=i+1)).date()   
                #print 3
                today_5 = EMA_Stock(stock, 10, dayIndex)
                today_10 = EMA_Stock(stock, 20, dayIndex)
                today_50 = EMA_Stock(stock, 50, dayIndex)
                yesterday_5 = EMA_Stock(stock, 10, day_before)
                yesterday_10 = EMA_Stock(stock, 20, day_before)
                yesterday_50 = EMA_Stock(stock, 50, day_before)
                is_ema_good = check_ema( ( today_5, today_10, today_50 ), ( yesterday_5, yesterday_10, yesterday_50 ) , stock, dayIndex)
                is_ema_good2 = check_ema2( ( today_5, today_10, today_50 ), ( yesterday_5, yesterday_10, yesterday_50 ) , stock, dayIndex)
                
                #print 4
                # check ForceIndex rule
                force_index_2 = ForceIndex( stock, 2, dayIndex )
                force_index_13 = ForceIndex( stock, 13, dayIndex )
                is_force_index_good = check_force_index( ( force_index_2, force_index_13 ) )
                #print 5
                # check Bollinger rule
                bollinger_band = BollingBand_Stock( stock, 20, dayIndex )
                is_bollinger_good = check_bollinger( bollinger_band, stock.closes[ dayIndex ] )
                is_bollinger_good2 = check_bollinger2( bollinger_band, stock.closes[ dayIndex ] )
                #print 6
                # check price rule
                is_price_good = check_price( stock.closes[ dayIndex ] )
                # check small pullback in uptrend
                is_pullback_good = check_small_pullback(stock, dayIndex)
                #print 7
                # check volume rule
                is_volume_good = check_volumes( stock, dayIndex )
                is_volume2_good = check_volumes2( stock.volumes[ dayIndex ] )
                #print 8
                # check Stochastic rule
                is_stochastic_good = check_stochastic( stock, 14, 3, 3, dayIndex )
                #print 9
                # is_ema_good = True
                # is_force_index_good = True
                # is_bollinger_good = True
                # is_price_good = True
                #is_volume_good = True
                #is_volume2_good = True
                #is_stochastic_good = True

                if (((is_ema_good or is_ema_good2) and is_bollinger_good) or (is_pullback_good and is_bollinger_good2)) and is_force_index_good and is_price_good and is_volume_good and is_volume2_good and is_stochastic_good:
                    highest_close_after = max( stock.closes[ dayIndex + 0 : dayIndex + 3] )
                    lowest_close_after = min( stock.closes[ dayIndex + 0 : dayIndex + 3] )
                    highest_high_after = max( stock.highs[ dayIndex + 0 : dayIndex + 3] )
                    output.write( str( highest_close_after / stock.closes[ dayIndex ] ) + ", " + str( highest_high_after /  stock.closes[ dayIndex ] ) + ", " + str( lowest_close_after /  stock.closes[ dayIndex ] ) + " ::: " )      # print the earning ratio
                    output.write(stock.ticker + ',' + str( stock.dates[ dayIndex ] ))
                    if(is_ema_good and is_bollinger_good):
                        output.write('--mid term')
                    if(is_ema_good2 and is_bollinger_good):
                        output.write('--long term')
                    if(is_pullback_good and is_bollinger_good2):
                        output.write('--short term')
                    output.write('\n')
                    total_count += 1
                    if highest_high_after /  stock.closes[ dayIndex ] < 1.02:
                        lost += lowest_close_after /  stock.closes[ dayIndex ]
                        lost_count += 1
                    else:
                        win += highest_close_after / stock.closes[ dayIndex ]
                        win_count += 1
                    print stock.ticker + ',' + str( stock.dates[ dayIndex ] )
        except:
            print key + ": not enough data for analysis"
    print 'finish';
    print 'loss rate:' + str(lost_count and (lost / lost_count) or 0 ) + ", loss picks:" + str( lost_count ) + ' win rate:' + str(win_count and (win / win_count) or 0 ) + ', win picks: ' + str( win_count )
    output.write('finish' + '\n')
    output.close() 

def check_ema( now_emas, before_emas , stock, dayIndex):
    #return 0
     #EMA 10 or 20 cross 50 and close price above EMA 50, mid term
    return now_emas[ 0 ] > before_emas[ 0 ] and now_emas[ 1 ] > before_emas[ 1 ] and (before_emas[ 0 ] < before_emas[2] or before_emas[1] < before_emas[2]) and (now_emas[ 0 ] >= now_emas[ 2 ] or now_emas[ 1 ] >= now_emas[ 2 ]) and stock.highs[ dayIndex ] >= now_emas[ 0 ]

def check_ema2(now_emas, before_emas , stock, dayIndex):
    return 0
    #EMA 10 cross 20, long term
    return before_emas[ 0 ] < before_emas[ 1 ] and now_emas[ 0 ] >= now_emas[ 1 ] and now_emas[ 0 ] < now_emas[ 2 ] and now_emas[ 1 ] < now_emas[ 2 ] 

def check_small_pullback(stock, dayIndex):
    #small pullback in uptrend, low risk and big profit, short term. not done yet
    return (((stock.closes[dayIndex-1] - stock.closes[dayIndex-2])/stock.closes[dayIndex-2]) >= 0.03) and ((stock.closes[dayIndex] - stock.closes[dayIndex-1]) < 0) and (((stock.closes[dayIndex-1] - stock.closes[dayIndex])/stock.closes[dayIndex-1]) <= 0.01)

def check_force_index( force_index_tuple ):
    return force_index_tuple[ 0 ] > 0 and force_index_tuple[ 1 ] > 0
    #return force_index_tuple[ 1 ] > 0

def check_bollinger( bollinger_band, close ):
    #return 0
    #return close < bollinger_band[ 1 ] and (bollinger_band[ 2 ] - bollinger_band[ 0 ]) >= 0.5
    return (bollinger_band[ 2 ] - bollinger_band[ 0 ]) >= 0.6

def check_bollinger2(bollinger_band, close):
    return close < bollinger_band[ 1 ] and (bollinger_band[ 2 ] - bollinger_band[ 0 ]) >= 0.5

def check_price( close ):
    return close > 1

def check_volumes( stock, dayIndex ):
    recent_max_volume = max( stock.volumes[ dayIndex - 2 : dayIndex ] )
    return recent_max_volume > 1.5 * Average_Volume( stock, 50, dayIndex )

def check_stochastic( stock, k_min_max_length, k_smooth_length, d_length, dayIndex ):
    pair = Stochastic_Stock( stock, k_min_max_length, k_smooth_length, d_length, dayIndex )
    return pair[ 0 ] <= 70

def check_volumes2( volume ):
    return volume > 30000

if __name__ == '__main__':
    folder = sys.argv[1]
    days = int(sys.argv[2])
    load_stocks(folder, days)
    #print stocks['AAPL'].repr_one_day(0)
    analyze()
        
    
