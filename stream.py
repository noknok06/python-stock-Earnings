import streamlit as st
import pandas as pd
import altair as alt
import csv
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px



class CSV:

    def read_csv():

        csv_data = []

        # Specify the path to your CSV file
        csv_file_path = 'result.csv'  # Replace 'your_file.csv' with the actual file path

        # Read the CSV file and store its contents in the list
        with open(csv_file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)

            for row in csv_reader:
                csv_data.append(row)

        return csv_data


lists = CSV.read_csv()

# 3列目から6列目までの要素を文字列から数値にキャストする
for row in lists:
    for i in range(3, len(row)):
        try:
            tmp = row[i].replace(",", "")
            tmp = tmp.replace("－", "-")
            if tmp == "-" or tmp == "None":
                tmp = 0
            row[i] = tmp
            # tmp = int(tmp)
        except Exception as e:
            print(e)

# 2列目だけを取り出す
category_column = [row[1] for row in lists]
category_column = sorted(list(set(category_column)))

st.set_page_config(
    page_title="Stock Analytics",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)


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

df = pd.DataFrame(lists)

# 表示する列の範囲を指定
start_col = 0
end_col = 8
df = df.iloc[:, start_col:end_col]
feature = ["code", "category", "name", "uri1", "uri2", "uri3", "uri4", "uri5"]
df.columns = feature

df['uri1'] = pd.to_numeric(df['uri1'], errors='coerce')
df['uri2'] = pd.to_numeric(df['uri2'], errors='coerce')
df['uri3'] = pd.to_numeric(df['uri3'], errors='coerce')
df['uri4'] = pd.to_numeric(df['uri4'], errors='coerce')
df['uri5'] = pd.to_numeric(df['uri5'], errors='coerce')

uri_df = df
uri_df.set_index('code', inplace=True)

st.title("売上カテゴリ平均")
feature = ["category", "uri1", "uri2", "uri3", "uri4", "uri5"]
df_selected = df[feature]
df_mean = df_selected.groupby("category").mean()[
    ['uri1', 'uri2', 'uri3', 'uri4', 'uri5']]

df_mean.sort_values(by='uri5', inplace=True)
st.dataframe(df_mean.round())

col1, col2 = st.columns(2)

with col1:
    st.title("企業別売上高推移")
    st.dataframe(df)

with col2:

    if option != None:
        st.title("売上カテゴリ平均チャート")
        # 行と列を入れ替え
        result_transposed = df_mean.T

        desired_row = df_mean.loc[option]

        tmp = np.array([desired_row["uri1"], desired_row["uri2"],
               desired_row["uri3"], desired_row["uri4"], desired_row["uri5"]])

        # Group data together
        hist_data = [tmp]

        group_labels = ['Group 1']

        # # Create distplot with custom bin_size
        # fig = ff.create_distplot(
        #     hist_data, group_labels, bin_size=[.1, .25, .5])

        # # Plot!
        # st.plotly_chart(fig, use_container_width=True)

        # Create a DataFrame for plotting
        df_plot = pd.DataFrame({'過去5年分': ['uri1', 'uri2', 'uri3', 'uri4', 'uri5'], '売上高': tmp})

        # Plotting the bar chart
        fig = px.bar(df_plot, x='過去5年分', y='売上高', title='売上推移')
        st.plotly_chart(fig, use_container_width=True)