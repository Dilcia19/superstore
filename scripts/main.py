"""
Streamlit app for Superstore Dashboard
"""

import streamlit as st
import pandas as pd
from superstore_analysis import profit_delta

store_records = pd.read_csv('data/sample_superstore_updated.csv')


col1, col2, col3= st.columns(3)

profit_delta_dict = profit_delta(store_records)

with col1:
    st.write("profits, 2016-2017")
    profits_2017 = profit_delta_dict['profits_2017']
    profit_pct_change_recent = profit_delta_dict['profit_pct_change_recent']
    st.metric(label="Profit % change recent", value=profits_2017, delta=profit_pct_change_recent)
    

with col2:
    st.write("sales, 2016-2017")
    sales_2017 = profit_delta_dict['profits_2017']
    sales_pct_change_recent = profit_delta_dict['sales_pct_change_recent']
    st.metric(label="Profit % change recent", value=sales_2017, delta=sales_pct_change_recent)

with col3:
    st.header("An owl")
