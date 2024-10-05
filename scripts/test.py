"""
Streamlit app for Superstore Dashboard
"""

import streamlit as st
import altair as alt
import pydeck as pdk
import plotly.express as px


import pandas as pd
import numpy as np
from superstore_analysis import profit_delta, repeat_customers, top_sub_categories_profit, top_sub_categories_sales
from superstore_analysis import profits_and_sales_by_state
from state_abbrev import states_abbreviation

#######################
# Page configuration
st.set_page_config(
    page_title="Superstore Dashboard",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded")

# Custom function to display metric with value and delta side-by-side
def custom_metric(label, value, delta_value):
    try:
        # Check if delta_value can be converted to a float
        delta_value = float(delta_value)
    except ValueError:
        delta_value = 0  # Default to 0 if conversion fails

    # Determine the arrow and color based on the delta_value
    if delta_value > 0:
        arrow = "▲"
        delta_color = "green"
    elif delta_value < 0:
        arrow = "▼"
        delta_color = "red"
    else:
        arrow = ""
        delta_color = "black"  # Neutral case

    st.markdown(f"""
    <div style='display: flex; justify-content: center; align-items: center; text-align: center;'>
        <div style='font-size: 1em;'>{label}</div>
        <div style='margin-left: 10px; font-size: 1.8em;'>
            {value} <span style='color: {delta_color}; font-size: 0.9em; margin-left: 5px;'>
            {arrow} {delta_value}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

store_records = pd.read_csv('data/sample_superstore_updated.csv', dtype={'year':int})

st.markdown("<h1 style='text-align: center; color: dark-blue;'>Super Store Dashboard</h1>", unsafe_allow_html=True)
st.write("\n")

with st.sidebar:
    st.title("Superstore Dashboard")
    st.write("The Super Store was founded at the end of 2013 and started selling products in 2014. The store has seen year over year growth in terms of sales and profits. With the elimination of a few key products, we will set up the super store to break record profits and sales in the upcoming years.")
    # selected_year = st.sidebar.selectbox("Select Year:", store_records["year"].unique())
    selected_year = st.sidebar.selectbox("Select Year:", np.sort(store_records["year"].unique()))
    

col1, col2, col3= st.columns(3)

profit_delta_dict = profit_delta(store_records)
repeat_order_pct, not_first_order = repeat_customers(store_records)

# Using the custom_metric function in each column
with col1:
    profits_2017 = profit_delta_dict['profits_2017']
    profit_pct_change_recent = profit_delta_dict['profit_pct_change_recent']
    custom_metric("Profit % change, 2016-2017", '${:,}'.format(profits_2017), profit_pct_change_recent)

with col2:
    sales_2017 = profit_delta_dict['sales_2017']
    sales_pct_change_recent = profit_delta_dict['sales_pct_change_recent']
    custom_metric("Sales % change,  2016-2017", '${:,}'.format(sales_2017), sales_pct_change_recent)

with col3:
    custom_metric("% Repeat Customers", f"{repeat_order_pct}%", '')
