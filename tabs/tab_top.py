import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px

from manage_csv import ManageCsv as cs
from manage_dataframe import ManageDataFrame as mdf
from manage_streamlit import ManageSt as mstl
from apis.web_datareader import WebDatareader as wd


class TabTop:

    def disp_page():

        stock_li = cs()
        stock_li.cleansing()
        lists = stock_li.data
        select_close = 0

        # 2列目だけを取り出す
        category_column = stock_li.cut_col(1)
        category_column = sorted(list(set(category_column[1:])))

        cam_li = pd.DataFrame(lists).iloc[:, [0]].values

        # リスト内包表記を使用して1次元のリストに変換
        new_array = [row[0] for row in cam_li]

        col1, col2, col3 = st.columns(3)

        with col1:

            # category
            option = st.selectbox(
                "カテゴリーを選択して下さい",
                (category_column),
                index=None,
                placeholder="Select contact method...",
            )

        with col2:

            cam_li = cam_li[1:]
            company_options = st.multiselect(
                '証券コードを選択して下さい', cam_li)

        with col3:
            # 売上カテゴリ平均
            uri_ave_checked = st.checkbox('売上カテゴリ平均　ON/OFF')

        if option == None:
            lists = [row for row in lists if row[1]]
        else:
            lists = [row for row in lists if row[1] == option]

        Cdf = mdf(lists)

        col1, col2 = st.columns(2)

        with col1:
            # 売上データ抽出
            start_col = 0
            end_col = 18
            Cdf.cut_range_col(start_col, end_col)

            # ヘッダー名設定
            feature = ["code", "category", "name",
                       "uri1", "uri2", "uri3", "uri4", "uri5",
                       "eiri1", "eiri2", "eiri3", "eiri4", "eiri5",
                       "kei1", "kei2", "kei3", "kei4", "kei5",
                       "dividend"]
            Cdf.dataf.columns = feature

            # 数値に変換
            Cdf.dataf['uri1'] = pd.to_numeric(
                Cdf.dataf['uri1'], errors='coerce')
            Cdf.dataf['uri2'] = pd.to_numeric(
                Cdf.dataf['uri2'], errors='coerce')
            Cdf.dataf['uri3'] = pd.to_numeric(
                Cdf.dataf['uri3'], errors='coerce')
            Cdf.dataf['uri4'] = pd.to_numeric(
                Cdf.dataf['uri4'], errors='coerce')
            Cdf.dataf['uri5'] = pd.to_numeric(
                Cdf.dataf['uri5'], errors='coerce')

            Cdf.dataf['eiri1'] = pd.to_numeric(
                Cdf.dataf['eiri1'], errors='coerce')
            Cdf.dataf['eiri2'] = pd.to_numeric(
                Cdf.dataf['eiri2'], errors='coerce')
            Cdf.dataf['eiri3'] = pd.to_numeric(
                Cdf.dataf['eiri3'], errors='coerce')
            Cdf.dataf['eiri4'] = pd.to_numeric(
                Cdf.dataf['eiri4'], errors='coerce')
            Cdf.dataf['eiri5'] = pd.to_numeric(
                Cdf.dataf['eiri5'], errors='coerce')

            Cdf.dataf['kei1'] = pd.to_numeric(
                Cdf.dataf['kei1'], errors='coerce')
            Cdf.dataf['kei2'] = pd.to_numeric(
                Cdf.dataf['kei2'], errors='coerce')
            Cdf.dataf['kei3'] = pd.to_numeric(
                Cdf.dataf['kei3'], errors='coerce')
            Cdf.dataf['kei4'] = pd.to_numeric(
                Cdf.dataf['kei4'], errors='coerce')
            Cdf.dataf['kei5'] = pd.to_numeric(
                Cdf.dataf['kei5'], errors='coerce')

            feature = ["category", "uri1", "uri2", "uri3", "uri4", "uri5"]
            df_selected = Cdf.dataf[feature]
            df_mean = df_selected.groupby("category").mean()[
                ['uri1', 'uri2', 'uri3', 'uri4', 'uri5']]

            df_mean.sort_values(by='uri5', inplace=True, ascending=False)
            df_mean = df_mean.round()

            if uri_ave_checked:

                st.subheader('売上カテゴリ平均', divider='rainbow')
                # チャート列追加
                df_mean.insert(len(df_mean.columns), 'charts', np.NaN)
                df_mean['charts'] = df_mean.apply(lambda row: [
                    row['uri1'], row['uri2'], row['uri3'], row['uri4'], row['uri5']], axis=1)
                # 一行目を削除
                # df_mean.drop('category', inplace=True)

                st.data_editor(
                    df_mean,
                    column_config={
                        "charts": st.column_config.LineChartColumn(
                            "売上高推移",
                            width="medium",
                            help="The sales volume in the last 6 months",
                        ),
                    },
                )

            st.subheader('企業別売上高推移', divider='rainbow')
            df_office = Cdf.dataf
            # チャート列追加
            df_office.insert(len(df_office.columns), 'charts', np.NaN)
            df_office['charts'] = df_office.apply(lambda row: [
                row['uri1'], row['uri2'], row['uri3'], row['uri4'], row['uri5']], axis=1)

            df_office.index = df_office["code"]

            feature = ["name", "category", "uri1", "uri2", "uri3", "uri4",
                       "uri5", "eiri1", "eiri2", "eiri3", "eiri4", "eiri5", "dividend", "charts"]
            df_selected = df_office[feature]

            df_selected.insert(0, 'Select', False)


            uri_col1, uri_col2 = st.columns(2)

            with uri_col1:
                uri_checked = st.checkbox('5年連続売上増')
            with uri_col2:
                uririe_checked = st.checkbox('5年連続増収増益')

            if uri_checked:
                df_selected = df_selected[
                    (df_selected['uri1'] < df_selected['uri2']) &
                    (df_selected['uri2'] < df_selected['uri3']) &
                    (df_selected['uri3'] < df_selected['uri4']) &
                    (df_selected['uri4'] < df_selected['uri5'])
                ]
            if uririe_checked:
                df_selected = df_selected[
                    (df_selected['uri1'] < df_selected['uri2']) &
                    (df_selected['uri2'] < df_selected['uri3']) &
                    (df_selected['uri3'] < df_selected['uri4']) &
                    (df_selected['uri4'] < df_selected['uri5']) &
                    (df_selected['eiri1'] < df_selected['eiri2']) &
                    (df_selected['eiri2'] < df_selected['eiri3']) &
                    (df_selected['eiri3'] < df_selected['eiri4']) &
                    (df_selected['eiri4'] < df_selected['eiri5'])
                ]

            if len(company_options) != 0:
                # df_selected = df_selected[df_selected['name'].isin(company_options)]
                arr = []
                for row in company_options:
                    arr.append(row[0])
                try:
                    df_selected = df_selected.loc[arr, :]
                except:
                    feature = ["name", "category", "dividend", "uri1",
                               "uri2", "uri3", "uri4", "uri5", "charts"]
                    df_selected = pd.DataFrame(columns=feature)

            try:
                # 一行目を削除
                df_selected.drop('code', inplace=True)
            except Exception as e:
                print(e)
                pass

            feature = ["Select", "name", "dividend", "category", "uri1", "uri2", "uri3",
                       "uri4", "uri5", "charts"]
            df_selected = df_selected[feature]

            df_selected.sort_values(by='uri5', inplace=True, ascending=False)
            edited_df = st.data_editor(
                df_selected,
                column_config={
                    "charts": st.column_config.LineChartColumn(
                        "売上高推移",
                        width="medium",
                        help="The sales volume in the last 6 months",
                    ),
                    "Select": st.column_config.CheckboxColumn(
                        "check",
                        help="Select your **favorite** widgets",
                        default=False,
                    ),
                },
            )

            try:
                if 'selecteds' not in st.session_state:
                    st.session_state.selecteds = edited_df
                changed_rows = df_selected[st.session_state.selecteds['Select']
                                           != edited_df['Select']]

                st.session_state.selecteds = edited_df
                selected_rows = edited_df[edited_df.Select]
            except Exception as e:
                st.session_state.selecteds = edited_df

                print(e)

                st.stop()

        with col2:

            try:
                selected_row = selected_rows[selected_rows["name"]
                                             == changed_rows["name"][0]]
                if not selected_rows.empty:
                    if selected_row.empty:
                        selected_row = selected_rows.head()

                    code = selected_row.index.values[0]
                    stock = wd.get_stock_data(code)
                    select_close = stock['Close'][0]

                    divide_rate = str(round(float(selected_row["dividend"][0])/select_close,2) * 100) + "%"
                    st.subheader(
                        '売上推移　' + selected_row['name'][0] + "　¥" + str(select_close) + "　" + str(divide_rate), divider='rainbow')
                    uri1 = selected_row['uri1'][0]
                    uri2 = selected_row['uri2'][0]
                    uri3 = selected_row['uri3'][0]
                    uri4 = selected_row['uri4'][0]
                    uri5 = selected_row['uri5'][0]

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric(label="昨年比４", value=uri2 -
                                  uri1, delta=str(((1-uri1/uri2)*100).round(3)) + "%")  # 指標
                    with col2:
                        st.metric(label="昨年比３", value=uri3 -
                                  uri2, delta=str(((1-uri2/uri3)*100).round(3)) + "%")  # 指標
                    with col3:
                        st.metric(label="昨年比２", value=uri4 -
                                  uri3, delta=str(((1-uri3/uri4)*100).round(3)) + "%")  # 指標
                    with col4:
                        st.metric(label="昨年比１", value=uri5 -
                                  uri4, delta=str(((1-uri4/uri5)*100).round(3)) + "%")  # 指標
            except Exception as e:
                print(e)

            if len(selected_rows) > 0:

                mstl.create_A(Cdf.dataf, selected_rows)        

        