from datetime import date

class Stock():
    def __init__(self, ticker, date, p_open, p_high, p_low, p_close, volumn):
    	self.ticker = ticker
    	self.date = date
    	self.p_open = p_open
    	self.p_high = p_high
        self.p_low = p_low
        self.p_close = p_close
        self.volumn = volumn

    def __str__(self):
    	return '%s, %s, %s, %s, %s, %s, %s' % (self.ticker, self.date, self.p_open, self.p_high, self.p_low, self.p_close, self.volumn)


if __name__ == '__main__':
    stock = Stock('AAPL', date(2012, 11, 30), 2.45, 2.56, 2.35, 2.41, 3000000)
    print str(stock)    	


