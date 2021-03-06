from datetime import date, datetime, timedelta
import math

CONST_IGNORE_RATIO = 3

def getStockPrice( stock, timeLength, baseIndex ):
    priceArray = stock.closes[ baseIndex - timeLength + 1 : baseIndex + 1 ]
    return priceArray

def EMA_Stock( stock, timeLength, dayIndex ):
    priceArray = getStockPrice( stock, timeLength * CONST_IGNORE_RATIO, dayIndex )
    return EMA( priceArray, timeLength )

def EMA( inputArray, length ):
    inputLength = len( inputArray )
    returnValue = 0
    k = float( 2 ) / ( length + 1 )
    for i in range( 0, inputLength ):
        returnValue = inputArray[ i ] * k + returnValue * ( 1 - k )
    return returnValue

def ForceIndex( stock, indexLength, dayIndex ):
    forceIndexArray = []
    baseIndex = dayIndex
    for i in range( indexLength * CONST_IGNORE_RATIO - 1, 0, -1 ):
        forceIndexArray.append( ( stock.closes[ baseIndex - i ] - stock.closes[ baseIndex - i - 1 ] ) * stock.volumes[ baseIndex - i ] )
    return EMA( forceIndexArray, indexLength )

def MA( inputArray ):
    sum = 0
    inputLength = len( inputArray )
    for i in inputArray:
        sum += i
    return float( sum ) / inputLength

def MA_Stock( stock, timeLength, dayIndex ):
    priceArray = getStockPrice( stock, timeLength, dayIndex )
    return MA( priceArray )

def BollingBand_Stock( stock, timeLength, dayIndex ):
    priceArray = getStockPrice( stock, timeLength, dayIndex )
    return BollingBand( priceArray )

def BollingBand( inputArray ):
    midBand = MA( inputArray )
    for i in range( 0, len( inputArray ) - 1 ):
        inputArray[ i ] -= midBand
        inputArray[ i ] = inputArray[ i ] ** 2
    std = math.sqrt( float( sum( inputArray ) ) / len( inputArray ) )
    upBand = midBand + 2 * std
    lowBand = midBand - 2 * std
    return ( lowBand, midBand, upBand )

def MACD_Line_Stock( stock, shortLength, longLength, dayIndex ):
    return EMA_Stock( stock, shortLength, dayIndex ) - EMA_Stock( stock, longLength, dayIndex )

def MACD_Stock( stock, shortLength, longLength, signalLength, dayIndex ):
    macdLines = []
    for i in range( signalLength * CONST_IGNORE_RATIO - 1, -1, -1 ):
        macdLines.append( MACD_Line_Stock( stock, shortLength, longLength, dayIndex - i ) )
    macdLine = macdLines[ -1 ]
    signal = EMA( macdLines, signalLength )
    histogram = macdLine - signal
    return ( macdLine, signal, histogram )

def Stochastic_K( stock, k_length, dayIndex ):
    baseIndex = dayIndex
    currentClose = stock.closes[ baseIndex ]
    highArray = stock.highs[ baseIndex - k_length + 1 : baseIndex + 1 ]
    lowArray = stock.lows[ baseIndex - k_length + 1 : baseIndex + 1 ]
    lowestLow = min( lowArray )
    highestHigh = max( highArray )
    return float( currentClose - lowestLow ) / ( highestHigh - lowestLow ) * 100

def Stochastic_Smoothed_K( ks, k_smooth_length, d_length ):
    smoothed_k = []
    for i in range( d_length ):
        smoothed_k.append( float( sum( ks[ i : i + k_smooth_length ] ) ) / k_smooth_length )
    return smoothed_k


def Stochastic_Stock( stock, k_min_max_length, k_smooth_length, d_length, dayIndex ):
    ks = []
    k_array_length = k_smooth_length + d_length - 1
    for i in range( k_array_length - 1, -1, -1 ):
        ks.append( Stochastic_K( stock, k_min_max_length, dayIndex - i ) )
    smoothed_k = Stochastic_Smoothed_K( ks, k_smooth_length, d_length )
    d = float( sum( smoothed_k ) ) / d_length
    k = smoothed_k[ -1 ]
    return ( k, d )

def Average_Volume( stock, length, dayIndex ):
    return float( sum( stock.volumes[ dayIndex - length + 1 : dayIndex + 1 ] ) ) /length