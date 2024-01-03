import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px

from manage_csv import ManageCsv as cs
from manage_dataframe import ManageDataFrame as mdf
from manage_streamlit import ManageSt as mstl

stock_li = cs()
stock_li.cleansing()
lists = stock_li.data

# 2列目だけを取り出す
category_column = stock_li.cut_col(1)
category_column = sorted(list(set(category_column)))

# ページ情報
st.set_page_config(
    page_title="Stock Analytics",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# select
option = st.selectbox(
    "Please select a category",
    (category_column),
    index=None,
    placeholder="Select contact method...",
)

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
               "kei1", "kei2", "kei3", "kei4", "kei5"]
    Cdf.dataf.columns = feature

    # 数値に変換
    Cdf.dataf['uri1'] = pd.to_numeric(Cdf.dataf['uri1'], errors='coerce')
    Cdf.dataf['uri2'] = pd.to_numeric(Cdf.dataf['uri2'], errors='coerce')
    Cdf.dataf['uri3'] = pd.to_numeric(Cdf.dataf['uri3'], errors='coerce')
    Cdf.dataf['uri4'] = pd.to_numeric(Cdf.dataf['uri4'], errors='coerce')
    Cdf.dataf['uri5'] = pd.to_numeric(Cdf.dataf['uri5'], errors='coerce')

    Cdf.dataf['eiri1'] = pd.to_numeric(Cdf.dataf['eiri1'], errors='coerce')
    Cdf.dataf['eiri2'] = pd.to_numeric(Cdf.dataf['eiri2'], errors='coerce')
    Cdf.dataf['eiri3'] = pd.to_numeric(Cdf.dataf['eiri3'], errors='coerce')
    Cdf.dataf['eiri4'] = pd.to_numeric(Cdf.dataf['eiri4'], errors='coerce')
    Cdf.dataf['eiri5'] = pd.to_numeric(Cdf.dataf['eiri5'], errors='coerce')

    Cdf.dataf['kei1'] = pd.to_numeric(Cdf.dataf['kei1'], errors='coerce')
    Cdf.dataf['kei2'] = pd.to_numeric(Cdf.dataf['kei2'], errors='coerce')
    Cdf.dataf['kei3'] = pd.to_numeric(Cdf.dataf['kei3'], errors='coerce')
    Cdf.dataf['kei4'] = pd.to_numeric(Cdf.dataf['kei4'], errors='coerce')
    Cdf.dataf['kei5'] = pd.to_numeric(Cdf.dataf['kei5'], errors='coerce')

    # 売上カテゴリ平均
    uri_ave_checked = st.checkbox('ON/OFF')

    feature = ["category", "uri1", "uri2", "uri3", "uri4", "uri5"]
    df_selected = Cdf.dataf[feature]
    df_mean = df_selected.groupby("category").mean()[
        ['uri1', 'uri2', 'uri3', 'uri4', 'uri5']]

    df_mean.sort_values(by='uri5', inplace=True)
    df_mean = df_mean.round()
    
    if uri_ave_checked:
    
        st.subheader('売上カテゴリ平均', divider='rainbow')


        # チャート列追加
        df_mean.insert(len(df_mean.columns), 'charts', np.NaN)
        df_mean['charts'] = df_mean.apply(lambda row: [
                                        row['uri1'], row['uri2'], row['uri3'], row['uri4'], row['uri5']], axis=1)

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

    feature = ["name","category", "uri1", "uri2", "uri3", "uri4", "uri5", "charts"]
    df_selected = df_office[feature]

    df_selected.insert(0, 'Select', False)

    uri_checked = st.checkbox('5年連続売上増')
    if uri_checked:
        df_selected = df_selected[
            (df_selected['uri1'] < df_selected['uri2']) & 
            (df_selected['uri2'] < df_selected['uri3']) & 
            (df_selected['uri3'] < df_selected['uri4']) & 
            (df_selected['uri4'] < df_selected['uri5'])
        ]
        
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
    selected_rows = edited_df[edited_df.Select]
with col2:

    if option != None:
        st.subheader('売上カテゴリ平均：チャート', divider='rainbow')
        # 行と列を入れ替え
        desired_row = df_mean.loc[option]

        # Group data together
        hist_data = np.array([desired_row["uri1"], desired_row["uri2"],
                              desired_row["uri3"], desired_row["uri4"], desired_row["uri5"]])

        group_labels = ['Group 1']

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(label="昨年比４", value=desired_row["uri2"] -
                      desired_row["uri1"], delta=str(((1-desired_row["uri1"]/desired_row["uri2"])*100).round(3)) + "%")  # 指標
        with col2:
            st.metric(label="昨年比３", value=desired_row["uri3"] -
                      desired_row["uri2"], delta=str(((1-desired_row["uri2"]/desired_row["uri3"])*100).round(3)) + "%")  # 指標
        with col3:
            st.metric(label="昨年比２", value=desired_row["uri4"] -
                      desired_row["uri3"], delta=str(((1-desired_row["uri3"]/desired_row["uri4"])*100).round(3)) + "%")  # 指標
        with col4:
            st.metric(label="昨年比１", value=desired_row["uri5"] -
                      desired_row["uri4"], delta=str(((1-desired_row["uri4"]/desired_row["uri5"])*100).round(3)) + "%")  # 指標

        df_plot = pd.DataFrame(
            {'過去5年分': ['uri1', 'uri2', 'uri3', 'uri4', 'uri5'], '売上高': hist_data})

        # Plotting the bar chart
        # fig = px.bar(df_plot, x='過去5年分', y='売上高')
        # st.plotly_chart(fig, use_container_width=True)


    if len(selected_rows)>0:
        mstl.create_A(Cdf.dataf, selected_rows)