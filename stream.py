import streamlit as st
from tabs.tab_top import TabTop 
from tabs.tab_campany_detail import TabCampanyDatail
from tabs.tab_portfolio import TabPortfolio

# ページ情報
st.set_page_config(
    page_title="Stock Analytics",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

tab1, tab2, tab3 = st.tabs(["トップ", "企業詳細", "ポートフォリオ分析"])

with tab1:

    TabTop.disp_page()

with tab2:

    TabCampanyDatail.disp_page()

with tab3:

    TabPortfolio.disp_page()

