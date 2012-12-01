def getStockPrice( stock, timeLength, date ):
	baseIndex = stock.get_index_of_date( date )
	priceArray = stock.closes[ baseIndex - timeLength + 1 : baseIndex + 1 ]
	return priceArray

def EMA_Stock( stock, timeLength, date ):
	priceArray = getStockPrice( stock, timeLength, date )
	return EMA( priceArray )

def EMA( inputArray ):
	inputLength = len( inputArray )
	returnValue = 0
	for i in range( 0, inputLength ):
		k = 2 / ( ( i + 1 ) + 1 )
		returnValue = inputArray[ i ] * k + datereturnValue * [ 1 - k ] 
	return returnValue

def ForceIndex( stock, indexLength, date ):
	forceIndexArray = []
	baseIndex = stock.get_index_of_date( date )
	for i in range( indexLength - 1, -1, -1 ):
		forceIndexArray.append( ( stock.closes[ baseIndex - i ] - stock.closes[ baseIndex - i - 1 ] ) * stock.volumns[ baseIndex - i ] )
	return EMA( forceIndexArray )

def MA( inputArray ):
	sum = 0
	inputLength = len( inputArray )
	for i in inputArray:
		sum += i
	return float( sum ) / inputLength

def MA_Stock( stock, timeLength, date ):
	priceArray = getStockPrice( stock, timeLength, date )
	return MA( priceArray )

def BollingBand_Stock( stock, timeLength, date ):
	priceArray = getStockPrice( stock, timeLength, date )
	return BollingBand( priceArray )

def BollingBand( inputArray ):
	midBand = MA( inputArray )
	for i in range(len( inputArray ) ):
		inputArray[ i ] -= midBand
		inputArray[ i ] = inputArray[ i ] ** 2
	std = math.sqrt( sum( inputArray ) / len( inputArray ) )
	upBand = midBand + std
	lowBand = midBand - std
	return ( lowBand, midBand, upBand )
