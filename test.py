import yfinance as yf
import pandas as pd

# 明星工の情報を取得
stock_code = "1976.T"

# 指定した証券コードの企業情報を取得(JSON形式)
ticker_info = yf.Ticker(stock_code)


# 取得した情報の出力
# バランスシート
print("********バランスシート********")
print(ticker_info.balancesheet)


# 配当
print("********配当********")
print(ticker_info.dividends)