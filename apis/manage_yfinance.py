import yfinance as yf

class ManageYfinance:

    def __init__(self, code):
        self.ticker_info = yf.Ticker(code + '.T')