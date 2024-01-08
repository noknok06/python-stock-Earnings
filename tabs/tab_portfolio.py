import streamlit as st
import pandas as pd

import manage_csv as ms
import datetime as dt
import plotly.express as px

from apis.web_datareader import WebDatareader as wdr
from apis.scraping_html import ScrapingHTML as scht


class TabPortfolio:

    def disp_page():
        # Check if 'data' key exists in session_state, if not, initialize it as an empty list
        if 'data' not in st.session_state:
            colms = (
                '証券コード', '会社名', 'カテゴリ', '購入数', '株価', '購入額'
            )
            st.session_state.data = pd.DataFrame(columns=colms)

        col1, col2 = st.columns(2)
        df_rate = st.session_state.data

        with col1:
            with st.form("add_stock"):
                stock_code = st.text_input('銘柄コード')
                stock_num = st.text_input('購入数')

                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit")

            if submitted:
                if stock_code == "" or stock_num == "":
                    st.warning("入力情報が不足しています")
                else:

                    df = ms.ManageCsv.read_csv()
                    select_df = df[df['code'] == int(stock_code)]
                    try:
                        category = select_df['category'].values[0]
                        name = select_df['name'].values[0]
                    except Exception as e:
                        # category = select_df['category'][0]
                        # name = select_df['name'][0]
                        print(e)
                        st.warning("株式銘柄が見つかりません")
                        st.stop()

                    df_symbol = wdr.get_stock_data(stock_code)
                    df_symbol = df_symbol.reset_index()
                    if 'Select' not in st.session_state.data.columns:
                        st.session_state.data.insert(0, 'Select', False)
                        st.session_state.data['Select'] = st.session_state.data['Select'].fillna(
                            False)
                    try:
                        close = df_symbol['Close'][0]
                        cstock = scht(stock_code)
                        soup = cstock.get_html_gaiyo()
                        new_data = {
                            'Select': False,
                            '証券コード': stock_code,
                            '会社名': name,
                            'カテゴリ': category,
                            '購入数': stock_num,
                            '株価': close,
                            '購入額': int(close)*int(stock_num),
                            # '発行済み株式数': ,
                        }

                        # st.session_state.data = st.session_state.data.append(
                        #     new_data, ignore_index=True)
                        new_data_df = pd.DataFrame([new_data])
                        st.session_state.data = pd.concat(
                            [st.session_state.data, new_data_df], ignore_index=True)

                    except Exception as e:
                        print(e)
                        st.warning("株式情報がありません")

                    df_rate = st.session_state.data[st.session_state.data['Select'] == False]
                    total = df_rate['購入額'].sum()
                    df_rate['割合'] = df_rate['購入額'] / total

                    st.caption("合計金額")
                    st.write(total)

        with col2:

            if len(st.session_state.data) > 0:

                edited_df = st.data_editor(
                    df_rate,
                    column_config={
                        "Select": st.column_config.CheckboxColumn(
                            "check",
                            help="Select your **favorite** widgets",
                            default=False,
                        ),
                    },
                )
                st.session_state.data = edited_df

        if not df_rate.empty:
            df_rate.index = df_rate['カテゴリ']
            fig1 = px.bar(df_rate, y='割合', x='カテゴリ', title='カテゴリ別購入額構成比率')

            # Streamlitアプリにプロットを追加
            st.plotly_chart(fig1, use_container_width=True)

        # 時価総額取得
        # 時価総額の合計値計算
        # 時価総額加重平均を取得
