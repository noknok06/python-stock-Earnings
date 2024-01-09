import pandas as pd
import yfinance as yf

# CSVファイル読み込み
df = pd.read_csv('./result.csv')

# 配当金を計算して新しい列 'dividend' に追加
for index, row in df.iterrows():
    try:
        code = row['code']
        stock = yf.Ticker(str(code) + '.T')

        # 配当金の計算（例として直近の配当を2倍にしていますが、実際の計算は必要に応じて変更してください）
        calculate_dividend = stock.dividends.iloc[-1]

        # 新しい 'dividend' 列を作成し、計算された配当金を格納
        df.at[index, 'dividend'] = calculate_dividend

        print(index)
    
    except Exception as e:
        print(e)

# 結果をCSVファイルに保存
df.to_csv('data_with_dividends.csv', index=False)
