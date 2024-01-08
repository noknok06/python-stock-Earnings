import streamlit as st
import pandas as pd

import os
import datetime as dt
import pandas_datareader.data as web
import numpy as np
import altair as alt

from apis.manage_yfinance import ManageYfinance as myf


class TabCampanyDatail:

    def disp_page():

        col1, col2 = st.columns(2)

        with col1:
            # CSSスタイルを適用して横幅を調整
            st.markdown(
                f"""
                <style>
                    div[data-baseweb="input"] {{
                        width: 150px;
                    }}
                </style>
                """,
                unsafe_allow_html=True
            )

            # 初期値を当日の1年前から当日までに設定
            end_date_default = dt.datetime.today().date()
            start_date_default = end_date_default - dt.timedelta(days=365)

            col1_2, col2_2, col3_2 = st.columns(3)

            with col1_2:

                code = st.text_input('銘柄コードを入力して下さい')

                if code == "":
                    return

            with col2_2:

                # カレンダーで日付の範囲を指定
                start_date = st.date_input('開始日を選択してください',
                                        value=start_date_default)

            with col3_2:

                end_date = st.date_input('終了日を選択してください',
                                        value=end_date_default)


            # 銘柄コード入力(7177はGMO-APです。)
            ticker_symbol = code
            ticker_symbol_dr = ticker_symbol + ".JP"

            # データ取得
        # try:
            df = web.DataReader(
                ticker_symbol_dr, data_source='stooq', start=start_date, end=end_date)

            df = df.reset_index()
            df_Close = df['Close']
            df_25ma = df['Close'].rolling(window=25).mean()
            # df_Date = df['Date'].astype('datetime64[D]')
            df_Date = df['Date']
            df_Volume = df['Volume']

            data = pd.DataFrame({
                'Date': df_Date,
                'Stock_Price': df_Close,
                '25ma': df_25ma,
                'Volume': df_Volume
                })
            # except Exception as e:
            #     print(e)

            #     st.warning("株式情報がありません")
            #     return

            # Y軸の最大値を指定
            min_y_value = df_Close.min()-100
            max_y_value = df_Close.max()+100

            # Altairチャートの作成
            line_chart = alt.Chart(data).mark_line().encode(
                x='Date:T',  # 日付を時間スケールとして指定
                y=alt.Y('Stock_Price:Q', scale=alt.Scale(
                    domain=(min_y_value, max_y_value))),
                color=alt.value('green')  # 線の色を指定
            )

            ma25_chart = alt.Chart(data).mark_line().encode(
                x='Date:T',  # 日付を時間スケールとして指定
                y=alt.Y('25ma:Q', scale=alt.Scale(
                    domain=(min_y_value, max_y_value))),
                color=alt.value('red')  # 線の色を指定
            )

            bar_chart = alt.Chart(data).mark_bar().encode(
                x='Date:T',  # 日付を時間スケールとして指定
                y='Volume:Q',  # 出来高の軸
                color=alt.value('orange')  # 棒グラフの色を指定
            )

            
            volume_on = st.toggle('出来高チャート')

            if volume_on:
                # 右側の軸を追加
                combined_chart = alt.layer(
                    bar_chart,
                    ma25_chart,
                    line_chart,
                ).resolve_scale(
                    y='independent'  # 左右の軸を独立させる
                ).configure_axisY(
                    title=None,  # Y軸のタイトルを非表示
                    ticks=True,  # Y軸の目盛りを非表示
                    labels=True  # Y軸のラベルを非表示
                )
            else:
                # 右側の軸を追加
                combined_chart = alt.layer(
                    ma25_chart,
                    line_chart,
                ).resolve_scale(
                    y='independent'  # 左右の軸を独立させる
                ).configure_axisY(
                    title=None,  # Y軸のタイトルを非表示
                    ticks=True,  # Y軸の目盛りを非表示
                    labels=True  # Y軸のラベルを非表示
                )

            # Streamlitで表示
            st.altair_chart(combined_chart, use_container_width=True)

        t_info = myf(ticker_symbol)

        with col2:

            st.subheader('四半期財務', divider='rainbow')

            try:
                quarterly_financials = t_info.ticker_info.quarterly_financials

                quarterly_financials = quarterly_financials.T
                quarterly_financials = quarterly_financials.reset_index()
                quarterly_financials['date'] = quarterly_financials['index'].dt.strftime('%Y-%m-%d')
                quarterly_financials.index = quarterly_financials['date']
                # quarterly_financials = quarterly_financials.reset_index()
                # 行の順番を反転させる
                quarterly_financials = quarterly_financials[::-1]
                quarterly_financials = quarterly_financials.T


                quarterly_financials.insert(len(quarterly_financials.columns), 'charts', np.NaN)
                quarterly_financials['charts'] = quarterly_financials.apply(lambda row: [
                                                row[0], row[1], row[2], row[3]], axis=1)
                quarterly_financials_copy = quarterly_financials.copy()                  
                quarterly_financials_copy.rename(index={
                        'Operating Income': '営業利益',
                        'Operating Revenue': '営業収益',
                        # 'Operating Expense': '営業費用',
                        'Gross Profit': '粗利益',
                        'Cost Of Revenue': '収益原価',
                        'Total Revenue': '総収益',
                    }, inplace=True)

                feature = [
                    '営業利益',
                    '営業収益',
                    # '営業費用',
                    '粗利益',
                    '収益原価',
                    '総収益',
                ]
                quarterly_financials_copy = quarterly_financials_copy.T
                quarterly_financials_copy = quarterly_financials_copy[feature]
                quarterly_financials_copy = quarterly_financials_copy.T
                edited_df = st.data_editor(
                    quarterly_financials_copy,
                    column_config={
                        "charts": st.column_config.LineChartColumn(
                            "各種推移",
                            width="medium",
                            help="The sales volume in the last 6 months",
                        )
                    },
                )

                data = t_info.ticker_info.dividends
                data = data.reset_index()
                data = data.sort_values(
                    by='Date', ascending=False)  # 'A' 列を基準にソート
                data['date'] = data['Date'].dt.strftime('%Y-%m')
                data.index = data['date']

                data = data['Dividends']
                top5_rows = data.head(5)  # 上位5つの行を抽出

                st.subheader('配当', divider='rainbow')
                st.write(top5_rows)
                try:
                    st.write(round(top5_rows[0] / df_Close[0] * 100, 2))
                except Exception as e:
                    print(e)
                    pass

            except Exception as e:
                print(e)
                st.warning("四半期データがありません")
                return

