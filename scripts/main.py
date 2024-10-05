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

# Custom CSS to reduce spacing and center content
st.markdown("""
<style>
    .main > div {
        padding-top: 0rem;
    }
    .stMetric {
        text-align: center;
    }
    .stMetric > div {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 0.5rem 0;
    }
    .stMetric label {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        min-height: 20px;
        font-size: 0.9em;
    }
    .stMetric .css-1wivap2 {
        font-size: 1.8rem;
    }
    h1 {
        margin-top: 0.5rem;
        margin-bottom: 0rem;
        font-size: 2.2rem;
    }
    .stHorizontalBlock {
        padding-top: 0;
    }
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0;
    }
</style>
""", unsafe_allow_html=True)

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

st.markdown(
    "<h1 style='text-align: center; color: dark-blue; margin-bottom: 0px; padding-bottom: 0px;'>Super Store Dashboard</h1>", 
    unsafe_allow_html=True)
st.write("\n")

with st.sidebar:
    st.title("Superstore Dashboard")
    st.write("- The Super Store was founded at the end of 2013 and started selling products in 2014.")
    st.write("- The store has seen year over year growth in terms of sales and profits.")
    st.write("- With the elimination of a few key products, we will set up the super store to break record profits and sales in the upcoming years.")
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

st.markdown("<hr style='margin-top: 10px;'>", unsafe_allow_html=True)

col4, col5, col6 = st.columns([1, 1, 2])

with col4:
    df = store_records[store_records['year'] == selected_year]
    top_subs = top_sub_categories_profit(df)

    st.header("Top 5 Sub-categories by Profit")

    # Create a bar chart with sorted bars
    chart = alt.Chart(top_subs).mark_bar().encode(
        x=alt.X('sub_category:N', sort='-y'),  # Sort x-axis based on y-values in descending order
        y=alt.Y('profit:Q', title='Profit'),
    ).properties(
        width=alt.Step(80)  # Adjust bar width as needed
    )

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)


with col5:
    df = store_records[store_records['year'] == selected_year]
    top_subs_sales = top_sub_categories_sales(df)
    
    st.header("Top 5 Sub-categories by Sales")
    # Create a bar chart with sorted bars
    chart = alt.Chart(top_subs_sales).mark_bar().encode(
        x=alt.X('sub_category:N', sort='-y'),  # Sort x-axis based on y-values in descending order
        y=alt.Y('sales:Q', title='Sales'),
    ).properties(
        width=alt.Step(80)  # Adjust bar width as needed
    )
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

with col6:
    df = store_records[store_records['year'] == selected_year]
    gp_states_profit = profits_and_sales_by_state(df)
    gp_states_profit['state_abbrev'] = gp_states_profit['state'].map(states_abbreviation)
    # create altair map
    st.header("Profits by State")
    # Create a map
    map = px.choropleth(gp_states_profit, locations='state_abbrev', locationmode='USA-states', color='profit', scope='usa', hover_name='state', color_continuous_scale='Blues')
    st.plotly_chart(map)

st.write("__________________________________________________________________")





    

 
 
