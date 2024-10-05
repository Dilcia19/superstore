"""
Streamlit app for Superstore Dashboard
"""

import streamlit as st
import altair as alt

import pandas as pd
from superstore_analysis import profit_delta, repeat_customers, top_sub_categories

store_records = pd.read_csv('data/sample_superstore_updated.csv')

st.markdown("<h1 style='text-align: center; color: dark-blue;'>Super Store Dashboard</h1>", unsafe_allow_html=True)
st.write("\n")

with st.sidebar:
    st.title("Superstore Dashboard")
    st.write("Navigation sidebar")
    selected_product = st.sidebar.selectbox("Select Year:", store_records["year"].unique())

col1, col2, col3= st.columns(3)

profit_delta_dict = profit_delta(store_records)
repeat_order_pct, not_first_order = repeat_customers(store_records)

with col1:
    profits_2017 = profit_delta_dict['profits_2017']
    profit_pct_change_recent = profit_delta_dict['profit_pct_change_recent']
    st.metric(label="Profit % change, 2016-2017", value='{:,}'.format(profits_2017), delta=profit_pct_change_recent)
    # show profits_2017 as number with comma

    

with col2:
    sales_2017 = profit_delta_dict['sales_2017']
    sales_pct_change_recent = profit_delta_dict['sales_pct_change_recent']
    st.metric(label="Sales % change,  2016-2017", value='{:,}'.format(sales_2017), delta=sales_pct_change_recent)

with col3:
    st.metric(label="% Repeat Customers", value=None, delta=repeat_order_pct)

st.write("__________________________________________________________________")

col4, col5, col6= st.columns(3)

with col4:
    df = store_records[store_records['year'] == selected_product]
    top_subs = top_sub_categories(df)

    # Create a bar chart
    chart = alt.Chart(top_subs).mark_bar().encode(
        x='sub_category',
        y='profit'
    )
    # Display the chart in Streamlit
    st.altair_chart(chart)

with col5:
    df = store_records[store_records['year'] == selected_product]
    top_subs = top_sub_categories(df)
    
    # Create a bar chart
    chart = alt.Chart(top_subs).mark_bar().encode(
        x='sub_category',
        y='profit'
    )
    # Display the chart in Streamlit
    st.altair_chart(chart)
with col6:
    df = store_records[store_records['year'] == selected_product]
    top_subs = top_sub_categories(df)
    # Create a bar chart
    chart = alt.Chart(top_subs).mark_bar().encode(
        x='sub_category',
        y='profit'
    )
    # Display the chart in Streamlit
    st.altair_chart(chart)

st.write("__________________________________________________________________")
