from datetime import date

class Stock():
    def __init__(self, ticker):
        self.ticker = ticker
        self.days = 0
        self.dates = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []

    def add_data(self, date, p_open, p_high, p_low, p_close, volumn):       
        self.dates.append(date)
        self.opens.append(float(p_open))
        self.highs.append(float(p_high))
        self.lows.append(float(p_low))
        self.closes.append(float(p_close))
        self.volumes.append(int(volumn))
        self.days += 1
    
    def get_index_of_date(self, day):
        for i in range(self.days-1, -1, -1):
            if self.dates[i] <= day:
                return i


    def repr_one_day(self, index):
        return '%s, %s, %s, %s, %s, %s, %s' \
        % (self.ticker, self.dates[index], self.opens[index], self.highs[index], \
          self.lows[index], self.closes[index], self.volumes[index])


if __name__ == '__main__':
    stock = Stock('ZNGA')
    stock.add_data(date(2012, 11, 30), 2.45, 2.56, 2.35, 2.41, 3000000)
    print stock.repr_one_day(0)
    print stock.get_index_of_date(date(2012, 11, 30))       


