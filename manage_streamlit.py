import streamlit as st
import pandas as pd


class ManageSt:

    def create_A(mst_df, select_df):

        select_codes = []
        for row in select_df.values:
            select_codes.append(row[1])

        columns = ["code", "category", "name",
                   "uri1", "uri2", "uri3", "uri4", "uri5", "chart",
                   "eiri1", "eiri2", "eiri3", "eiri4", "eiri5",
                   "kei1", "kei2", "kei3", "kei4", "kei5"]
        df = pd.DataFrame(columns=columns)

        for val in mst_df.values:
            if val[2] in select_codes:
                new_row_data = pd.Series({
                    "code": val[0], "category": val[1], "name": val[2],
                    "uri1": val[3], "uri2": val[4], "uri3": val[5], "uri4": val[6], "uri5": val[7],
                    "eiri1": val[8], "eiri2": val[9], "eiri3": val[10], "eiri4": val[11], "eiri5": val[12],
                    "kei1": val[13], "kei2": val[14], "kei3": val[15], "kei4": val[16], "kei5": val[17]
                })

                # select_df = select_df.append(new_row_data,ignore_index=True)
                # df = df.append(new_row_data, ignore_index=True)
                df = pd.concat([df, new_row_data], ignore_index=True, axis=0)

        # df = pd.DataFrame(select_df, index=columns)

        uri_feature = ["code", "uri1", "uri2", "uri3", "uri4", "uri5"]
        eiri_feature = ["code", "eiri1", "eiri2", "eiri3", "eiri4", "eiri5"]
        kei_feature = ["code", "kei1", "kei2", "kei3", "kei4", "kei5"]

        uri_chart_df = df[uri_feature]
        uri_chart_df = uri_chart_df.set_index("code")
        uri_chart_df = uri_chart_df.T

        eiri_chart_df = df[eiri_feature]
        eiri_chart_df = eiri_chart_df.set_index("code")
        eiri_chart_df = eiri_chart_df.T

        kei_chart_df = df[kei_feature]
        kei_chart_df = kei_chart_df.set_index("code")
        kei_chart_df = kei_chart_df.T

        st.subheader('企業別チャート', divider='rainbow')
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 売上高")
            st.line_chart(uri_chart_df, height=400)

        with col2:
            st.markdown("#### 営業利益")
            st.line_chart(eiri_chart_df, height=400)

        with col3:
            st.markdown("#### 経常利益")
            st.line_chart(kei_chart_df, height=400)
