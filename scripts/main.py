"""
Streamlit app for Superstore Dashboard
"""

import streamlit as st
import altair as alt
import pydeck as pdk
import plotly.express as px


import pandas as pd
from superstore_analysis import profit_delta, repeat_customers, top_sub_categories_profit, top_sub_categories_sales
from superstore_analysis import profits_and_sales_by_state
from state_abbrev import states_abbreviation

#######################
# Page configuration
st.set_page_config(
    page_title="US Population Dashboard",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded")

store_records = pd.read_csv('data/sample_superstore_updated.csv')

st.markdown("<h1 style='text-align: center; color: dark-blue;'>Super Store Dashboard</h1>", unsafe_allow_html=True)
st.write("\n")

with st.sidebar:
    st.title("Superstore Dashboard")
    st.write("The Super Store was founded at the end of 2013 and started selling products in 2014. The store has seen year over year growth in terms of sales and profits. With the elimination of a few key products, we will set up the super store to break record profits and sales in the upcoming years.")
    selected_product = st.sidebar.selectbox("Select Year:", store_records["year"].unique())

col1, col2, col3= st.columns(3)

profit_delta_dict = profit_delta(store_records)
repeat_order_pct, not_first_order = repeat_customers(store_records)

with col1:
    profits_2017 = profit_delta_dict['profits_2017']
    profit_pct_change_recent = profit_delta_dict['profit_pct_change_recent']
    st.metric(label="Profit % change, 2016-2017", value='${:,}'.format(profits_2017), delta=profit_pct_change_recent)
    # show profits_2017 as number with comma

    

with col2:
    sales_2017 = profit_delta_dict['sales_2017']
    sales_pct_change_recent = profit_delta_dict['sales_pct_change_recent']
    st.metric(label="Sales % change,  2016-2017", value='${:,}'.format(sales_2017), delta=sales_pct_change_recent)

with col3:
    st.metric(label="% Repeat Customers", value=f"{repeat_order_pct}%", delta=None)

st.write("__________________________________________________________________")

# col4, col5, col6= st.columns(3)
col4, col5 = st.columns(2)

with col4:
    df = store_records[store_records['year'] == selected_product]
    top_subs = top_sub_categories_profit(df)

    st.header("Top 5 Sub-categories by Profit")
    # Create a bar chart
    chart = alt.Chart(top_subs).mark_bar().encode(
        x='sub_category',
        y='profit'
    )
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

with col5:
    df = store_records[store_records['year'] == selected_product]
    top_subs_sales = top_sub_categories_sales(df)
    
    st.header("Top 5 Sub-categories by Sales")
    # Create a bar chart
    chart = alt.Chart(top_subs_sales).mark_bar().encode(
        x='sub_category',
        y='sales'
    )
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

st.write("__________________________________________________________________")

gp_states_profit, gp_states_sales = profits_and_sales_by_state(store_records)
gp_states_profit['state_abbrev'] = gp_states_profit['state'].map(states_abbreviation)
gp_states_sales['state_abbrev'] = gp_states_sales['state'].map(states_abbreviation)

left, right = st.columns(2)
if left.button("Sales by State", use_container_width=True):
    left.markdown("You clicked the sales by state button.")
    print("You clicked the sales by state button.")
    # map gp_states_sales by us state and sales
    st.write(gp_states_sales)
    # Create a map
    map_data = gp_states_sales[['state_abbrev', 'sales']]
    view_state = pdk.ViewState(latitude=37.8, longitude=-96, zoom=3, pitch=0)
    layer = pdk.Layer('ChoroplethLayer', data=map_data, get_fill_color='[0, sales/1000000, 0, 100]', get_line_color=[0, 0, 0], auto_highlight=True, get_line_width=200)
    map = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', initial_view_state=view_state, layers=[layer])
    st.pydeck_chart(map)
    
if right.button("Profits by State", use_container_width=True):
    right.markdown("You clicked the profits by state button.")
    print("You clicked the profits by state button.")
 
