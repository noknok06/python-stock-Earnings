import streamlit as st
import pandas as pd

class TabPortfolio:

    def disp_page():
        # Check if 'data' key exists in session_state, if not, initialize it as an empty list
        if 'data' not in st.session_state:
            st.session_state.data = []

        with st.form("add_stock"):
            st.write("銘柄コード")
            stock_code = st.text_input('stock_code')
            st.write("購入数")
            stock_num = st.text_input('stock_num')

            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")

            if submitted:
                st.session_state.data.append({'stock_code': stock_code, 'stock_num': stock_num})

        # Display the dataframe outside the form
        st.dataframe(pd.DataFrame(st.session_state.data))
