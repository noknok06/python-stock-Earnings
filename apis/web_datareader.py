import pandas_datareader.data as web
import datetime as dt

class WebDatareader:

    def get_stock_data(stock_code):

        # データ取得
        end_date = dt.datetime.today().date()
        start_date = end_date - dt.timedelta(days=7)

        ticker_symbol_dr = stock_code + ".JP"
        df_symbol = web.DataReader(
            ticker_symbol_dr, data_source='stooq', start=start_date, end=end_date)

        return df_symbol