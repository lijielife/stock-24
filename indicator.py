from datetime import date, datetime, timedelta
import math

CONST_IGNORE_RATIO = 3

def getStockPrice( stock, timeLength, day ):
    baseIndex = stock.get_index_of_date( day )
    priceArray = stock.closes[ baseIndex - timeLength + 1 : baseIndex + 1 ]
    return priceArray

def EMA_Stock( stock, timeLength, day ):
    priceArray = getStockPrice( stock, timeLength * CONST_IGNORE_RATIO, day )
    return EMA( priceArray, timeLength )

def EMA( inputArray, length ):
    inputLength = len( inputArray )
    returnValue = 0
    k = float( 2 ) / ( length + 1 )
    for i in range( 0, inputLength ):
        returnValue = inputArray[ i ] * k + returnValue * ( 1 - k )
    return returnValue

def ForceIndex( stock, indexLength, day ):
    forceIndexArray = []
    baseIndex = stock.get_index_of_date( day )
    for i in range( indexLength * CONST_IGNORE_RATIO - 1, 0, -1 ):
        forceIndexArray.append( ( stock.closes[ baseIndex - i ] - stock.closes[ baseIndex - i - 1 ] ) * stock.volumes[ baseIndex - i ] )
    return EMA( forceIndexArray, indexLength )

def MA( inputArray ):
    sum = 0
    inputLength = len( inputArray )
    for i in inputArray:
        sum += i
    return float( sum ) / inputLength

def MA_Stock( stock, timeLength, day ):
    priceArray = getStockPrice( stock, timeLength, day )
    return MA( priceArray )

def BollingBand_Stock( stock, timeLength, day ):
    priceArray = getStockPrice( stock, timeLength, day )
    return BollingBand( priceArray )

def BollingBand( inputArray ):
    midBand = MA( inputArray )
    for i in range( 0, len( inputArray ) - 1 ):
        inputArray[ i ] -= midBand
        inputArray[ i ] = inputArray[ i ] ** 2
    std = math.sqrt( float( sum( inputArray ) ) / len( inputArray ) )
    upBand = midBand + std
    lowBand = midBand - std
    return ( lowBand, midBand, upBand )

def MACD_Line_Stock( stock, shortLength, longLength, day ):
    return EMA_Stock( stock, shortLength, day ) - EMA_Stock( stock, longLength, day )

def MACD_Stock( stock, shortLength, longLength, signalLength, day ):
    macdLines = []
    for i in range( signalLength * CONST_IGNORE_RATIO - 1, -1, -1 ):
        macdLines.append( MACD_Line_Stock( stock, shortLength, longLength, day - timedelta( days = i ) ) )
    macdLine = macdLines[ -1 ]
    signal = EMA( macdLines, signalLength )
    histogram = macdLine - signal
    return ( macdLine, signal, histogram )

def Stochastic_K( stock, k_length, day ):
    print 1.5
    baseIndex = stock.get_index_of_date( day )
    currentClose = stock.closes[ baseIndex ]
    print 1.6
    highArray = stock.highs[ baseIndex - k_length + 1 : baseIndex + 1 ]
    lowArray = stock.lows[ baseIndex - k_length + 1 : baseIndex + 1 ]
    print 1.7
    lowestLow = min( lowArray )
    highestHigh = max( highArray )
    print 1.8
    return float( currentClose - lowestLow ) / ( highestHigh - lowestLow ) * 100

def Stochastic_Smoothed_K( ks, k_smooth_length, d_length ):
    smoothed_k = []
    print 2.1
    for i in range( d_length ):
        print str( i ) + ", " + str( k_smooth_length ) + ", " + str( len( ks ) )
        smoothed_k.append( float( sum( ks[ i : i + k_smooth_length ] ) ) / k_smooth_length )
    print 2.3
    return smoothed_k


def Stochastic_Stock( stock, k_min_max_length, k_smooth_length, d_length, day ):
    ks = []
    k_array_length = k_smooth_length + d_length - 1
    print str( 1 ) + ", " + str( k_array_length )
    for i in range( k_array_length - 1, -1, -1 ):
        ks.append( Stochastic_K( stock, k_min_max_length, day - timedelta( days = i ) ) )
    print 2
    smoothed_k = Stochastic_Smoothed_K( ks, k_smooth_length, d_length )
    print 3
    d = float( sum( smoothed_k ) ) / d_length
    k = smoothed_k[ -1 ]
    return ( k, d )

def Average_Volume( stock, length, day ):
    dayIndex = stock.get_index_of_date( day )
    return float( sum( stock.volumes[ dayIndex - length + 1 : dayIndex + 1 ] ) ) /length