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

st.markdown("""
<style>
.stMetric {
    text-align: center;
}
.stMetric > div {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
}
.stMetric label {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    min-height: 50px;  /* Adjust this value as needed */
}
</style>
""", unsafe_allow_html=True)


store_records = pd.read_csv('data/sample_superstore_updated.csv')

st.markdown("<h1 style='text-align: center; color: dark-blue;'>Super Store Dashboard</h1>", unsafe_allow_html=True)
st.write("\n")

with st.sidebar:
    st.title("Superstore Dashboard")
    st.write("The Super Store was founded at the end of 2013 and started selling products in 2014. The store has seen year over year growth in terms of sales and profits. With the elimination of a few key products, we will set up the super store to break record profits and sales in the upcoming years.")
    selected_year = st.sidebar.selectbox("Select Year:", store_records["year"].unique())

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
# col4, col5, col6 = st.columns(3)
col4, col5, col6 = st.columns([1, 1, 2])

with col4:
    df = store_records[store_records['year'] == selected_year]
    top_subs = top_sub_categories_profit(df)

    st.header("Top 5 Sub-categories by Profit")

    # Create a bar chart with sorted bars
    chart = alt.Chart(top_subs).mark_bar().encode(
        x=alt.X('sub_category:N', sort='-y'),  # Sort x-axis based on y-values in descending order
        y=alt.Y('profit:Q', title='Profit'),
        # color=alt.Color('sub_category:N', legend=None)  # Optional: color bars by sub-category
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
    map = px.choropleth(gp_states_profit, locations='state_abbrev', locationmode='USA-states', color='profit', scope='usa', hover_name='state', color_continuous_scale='Viridis')
    st.plotly_chart(map)
  

# with col6:  
#     st.write("hello")



st.write("__________________________________________________________________")





    

 
 
