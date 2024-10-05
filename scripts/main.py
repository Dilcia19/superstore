"""
Streamlit app for Superstore Dashboard
"""

import streamlit as st
import pandas as pd
from superstore_analysis import profit_delta, repeat_customers

store_records = pd.read_csv('data/sample_superstore_updated.csv')


col1, col2, col3= st.columns(3)

profit_delta_dict = profit_delta(store_records)
repeat_order_pct, not_first_order = repeat_customers(store_records)

with col1:
    profits_2017 = profit_delta_dict['profits_2017']
    profit_pct_change_recent = profit_delta_dict['profit_pct_change_recent']
    st.metric(label="Profit % change, 2016-2017", value=profits_2017, delta=profit_pct_change_recent)
    

with col2:
    sales_2017 = profit_delta_dict['sales_2017']
    sales_pct_change_recent = profit_delta_dict['sales_pct_change_recent']
    st.metric(label="Sales % change,  2016-2017", value=sales_2017, delta=sales_pct_change_recent)

with col3:
    st.metric(label="% Repeat Customers", value=None, delta=repeat_order_pct)
