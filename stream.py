import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px

from manage_csv import ManageCsv as cs
from manage_dataframe import ManageDataFrame as mdf

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
    end_col = 8
    df = Cdf.cut_range_col(start_col, end_col)

    # ヘッダー名設定
    feature = ["code", "category", "name",
               "uri1", "uri2", "uri3", "uri4", "uri5"]
    df.columns = feature

    # 数値に変換
    df['uri1'] = pd.to_numeric(df['uri1'], errors='coerce')
    df['uri2'] = pd.to_numeric(df['uri2'], errors='coerce')
    df['uri3'] = pd.to_numeric(df['uri3'], errors='coerce')
    df['uri4'] = pd.to_numeric(df['uri4'], errors='coerce')
    df['uri5'] = pd.to_numeric(df['uri5'], errors='coerce')

    # 売上カテゴリ平均
    st.subheader('売上カテゴリ平均', divider='rainbow')
    feature = ["category", "uri1", "uri2", "uri3", "uri4", "uri5"]
    df_selected = df[feature]
    df_mean = df_selected.groupby("category").mean()[
        ['uri1', 'uri2', 'uri3', 'uri4', 'uri5']]

    df_mean.sort_values(by='uri5', inplace=True)
    df_mean = df_mean.round()

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
                # y_min=0,
                # y_max=100,
            ),
        },
    )


    st.subheader('企業別売上高推移', divider='rainbow')
    df.index = df["code"]
    feature = ["name","category", "uri1", "uri2", "uri3", "uri4", "uri5"]
    df_selected = df[feature]

    st.data_editor(df_selected)



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
        fig = px.bar(df_plot, x='過去5年分', y='売上高')
        st.plotly_chart(fig, use_container_width=True)
