from datetime import date, datetime, timedelta

def getStockPrice( stock, timeLength, day ):
    baseIndex = stock.get_index_of_date( day )
    priceArray = stock.closes[ baseIndex - timeLength + 1 : baseIndex + 1 ]
    return priceArray

def EMA_Stock( stock, timeLength, day ):
    priceArray = getStockPrice( stock, timeLength, day )
    return EMA( priceArray )

def EMA( inputArray ):
    inputLength = len( inputArray )
    print str( inputLength ) + str( inputArray )
    returnValue = 0
    for i in range( 0, inputLength ):
        k = float( 2 ) / ( ( i + 1 ) + 1 )
        returnValue = inputArray[ i ] * k + returnValue * ( 1 - k )
        print str( returnValue ) + ", " + str( k ) + ", " + str( i )
    return returnValue

def ForceIndex( stock, indexLength, day ):
    forceIndexArray = []
    baseIndex = stock.get_index_of_date( day )
    for i in range( indexLength - 1, 0, -1 ):
        forceIndexArray.append( ( stock.closes[ baseIndex - i ] - stock.closes[ baseIndex - i - 1 ] ) * stock.volumes[ baseIndex - i ] )
    return EMA( forceIndexArray )

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
    for i in range( signalLength - 1, -1, -1 ):
        macdLines.append( MACD_Line_Stock( stock, shortLength, longLength, day - timedelta( days = i ) ) )
    macdLine = macdLines[ -1 ]
    signal = EMA( macdLines )
    histogram = macdLine - signal
    return ( macdLine, signal, histogram )

def Stochastic_K( stock, k_length, day ):
    baseIndex = stock.get_index_of_date( day )
    currentClose = stock.closes[ baseIndex ]
    highArray = stock.highs[ baseIndex - timeLength + 1 : baseIndex + 1 ]
    lowArray = stock.lows[ baseIndex - timeLength + 1 : baseIndex + 1 ]
    lowestLow = min( lowArray )
    highestHigh = max( highArray )
    return float( currentClose - lowestLow ) / ( highestHigh - lowestLow ) * 100

def Stochastic_Stock( stock, k_length, d_length, day ):
    ks = []
    for i in range( d_length ):
        ks.append( Stochastic_K( stock, k_length, day ) )
    d = float( sum( ks ) ) / d_length
    return ( ks[ -1 ], d )
