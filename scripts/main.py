"""
Streamlit app for Superstore Dashboard
"""

import streamlit as st
import altair as alt
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np
from superstore_analysis import *
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
        margin-top: 0.25rem;
        margin-bottom: 0rem;
        font-size: 2.rem;
    }
    .stHorizontalBlock {
        padding-top: 0;
        padding-bottom: 0;
    }
    .block-container {
        padding-top: 10px;
        padding-bottom: 0;
    }

</style>
""", unsafe_allow_html=True)

# Custom function to display metric with value and delta side-by-side
def custom_metric(label, value, delta_value, repeat_customer):
    try:
        # Check if delta_value can be converted to a float
        delta_value = float(delta_value)
    except ValueError:
        delta_value = 0  # Default to 0 if conversion fails

    # Determine the arrow and color based on the delta_value
    if delta_value > 0:
        arrow = "▲"
        delta_color = "green"
        delta_text = f"{delta_value}%"
    elif delta_value < 0:
        arrow = "▼"
        delta_color = "red"
        delta_text = f"{delta_value}%"
    else:
        if repeat_customer:
            delta_value = ""
            arrow = ""
            delta_color = "black"
            delta_text = ""
        arrow = ""
        delta_color = "black"  # Neutral case

    st.markdown(f"""
    <div style='display: flex; justify-content: center; align-items: center; text-align: center;'>
        <div style='font-size: 1em;'>{label}</div>
        <div style='margin-left: 10px; font-size: 1.8em;'>
            {value} <span style='color: {delta_color}; font-size: 0.9em; margin-left: 5px;'>
            {arrow} {delta_text}</span>
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

    st.write("The Super Store was founded in 2014 and has seen year over year growth in sales and profits. With the elimination of a few key products and unprofitable geographical markets, the super store will generate record profits and sales for years to come.")

    selected_year = st.sidebar.selectbox("Select Year:", np.sort(store_records["year"].unique())[::-1])
    df = store_records[store_records['year'] == selected_year]
    high_profit_products, bottom_5_low_profit = high_profit_products(df)

    st.header(f"These five products brought in the most profit in {selected_year}")

    for i in range(1, 6):
        # Use markdown with HTML to color the profit in green
        profit = int(high_profit_products.iloc[i-1]['profit'])
        product_name = high_profit_products.iloc[i-1]['product_name']
        sales = int(high_profit_products.iloc[i-1]['sales'])
        percent_margin = int(high_profit_products.iloc[i-1]['percent_margin'])
        st.markdown(f"""
            <p style='margin-bottom: 0px;'>{i}: <strong>{product_name}</strong></p>
            <p style='margin-bottom: 0px;'>$ <span style='color:blue;'>{sales:,} </span>in sales, $ <span style='color:green;'>{profit:,} </span>in profits, profit margin: <span style='color:blue;'>{percent_margin}%</span></p>
        """, unsafe_allow_html=True)

    st.header(f"These five products brought in the least profit in {selected_year}")
    for i in range(1, 6):
        # Use markdown with HTML to color the profit in green
        profit = int(bottom_5_low_profit.iloc[i-1]['profit'])
        product_name = bottom_5_low_profit.iloc[i-1]['product_name']
        sales = int(bottom_5_low_profit.iloc[i-1]['sales'])
        percent_margin = int(bottom_5_low_profit.iloc[i-1]['percent_margin'])
        st.markdown(f"""
            <p style='margin-bottom: 0px;'>{i}: <strong>{product_name}</strong></p>
            <p style='margin-bottom: 0px;'>$ <span style='color:blue;'>{sales:,} </span>in sales, $ <span style='color:red;'>{profit:,} </span>in profits, profit margin: <span style='color:blue;'>{percent_margin}%</span></p>
        """, unsafe_allow_html=True)
    
    
col1, col2, col3= st.columns(3)

profit_delta_dict = profit_delta(store_records)
repeat_order_pct = repeat_customers(store_records)

# Using the custom_metric function in each column
with col1:
    sales_2017 = profit_delta_dict['sales_2017']
    sales_pct_change_recent = profit_delta_dict['sales_pct_change_recent']
    custom_metric("Sales,\n  2016-2017", '${:,}'.format(sales_2017), sales_pct_change_recent, False)

with col2:
    profits_2017 = profit_delta_dict['profits_2017']
    profit_pct_change_recent = profit_delta_dict['profit_pct_change_recent']
    custom_metric("Profit,\n 2016-2017", '${:,}'.format(profits_2017), profit_pct_change_recent, False)

with col3:
    custom_metric("Repeat Customers Total:", f"{repeat_order_pct}%", '', True)


st.markdown("<hr style='margin-top: 10px;'>", unsafe_allow_html=True)

col4, col5, col6 = st.columns([2, 1, 1])

with col4:
    # with col4:
    df = store_records[store_records['year'] == selected_year]
    top_subs = top_sub_categories_sales(df)
    
    # Melt the dataframe to long format for easier plotting
    melted_df = pd.melt(top_subs, id_vars=['sub_category'], value_vars=['sales', 'profit'], var_name='Metric', value_name='Value')

    # Define custom colors for sales and profit
    color_scale = alt.Scale(domain=['sales', 'profit'], range=['#0029ff', '#ff0000'])

    # Create the chart
    chart = alt.Chart(melted_df).mark_bar().encode(
        x=alt.X('sub_category:N', title='Sub-category', sort='-y'),  # Sub-category axis
        y=alt.Y('Value:Q', title='Amount in Sales/Profit'),  # Amount axis
        color=alt.Color('Metric:N', scale=color_scale, sort=['sales', 'profit']),  # Custom colors for sales and profit
        xOffset=alt.XOffset('Metric:N', sort=['sales', 'profit']),  # Ensure sales comes first in the offset
        tooltip=[alt.Tooltip('sub_category:N', title='Sub-category'),
                 alt.Tooltip('Metric:N', title='Metric'),
                 alt.Tooltip('Value:Q', title='Amount', format=',')]  # Add comma format to the Value
    ).properties(
        width=alt.Step(40),
        height=350,
        title="Sales and profits, top 5 categories"
    )

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

with col5:
    df = store_records[store_records['year'] == selected_year]
    top_5_high_sales_categories = high_sales_categories(df)

    # This chart became top 5 high sales & profit categories
    df = top_5_high_sales_categories
    
    # Prepare the data for the chart
    sales_total = sum(df['distribution of sales'])
    profit_total = sum(df['distribution of profit'])
    
    # Normalize sales and profit so they don't exceed 100% when combined
    df['normalized_sales'] = df['distribution of sales'] / sales_total * 100
    df['normalized_profit'] = df['distribution of profit'] / profit_total * 100
    
    # Create the chart data
    chart_data = pd.DataFrame({
        'category': df['category'].tolist() * 2,  # Duplicate categories for both Sales and Profit
        'value': df['normalized_sales'].tolist() + df['normalized_profit'].tolist(),  # Combine normalized sales and profit values
        'type': ['Sales'] * len(df) + ['Profit'] * len(df)  # Indicate type (Sales or Profit)
    })
    
    # Create the sunburst chart with updated color scheme
    fig = px.sunburst(
        chart_data,
        path=['type', 'category'],  # Define hierarchy: first 'type' (Sales or Profit), then 'category'
        values='value',  # Use the normalized value for size
        title="Category Sales and Profit Distribution",
        color='type',  # Color by type (Sales, Profit)
        color_discrete_map={'Sales': '#0029ff', 'Profit': '#ff0000'}  # Updated colors: Blue for Sales, Red for Profit
    )
    
    # Update traces to show both labels and values for child nodes (categories)
    fig.update_traces(
        texttemplate='<b>%{label}</b><br>%{value:.1f}%',  # Show percentages with 1 decimal point
        hovertemplate='<b>Distribution: %{value:.1f}%</b><br>%{label}'  # Show label and value for each segment
    )
    
    # Update the layout
    fig.update_layout(
        title_font_size=14,
        width=350,
        height=350,
        margin=dict(t=30, l=0, r=0, b=0)
    )
    
    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True, key="donut1")



with col6:
    df = store_records[store_records['year'] == selected_year]
    top_5_high_profit_segments = high_profit_segments(df)
    df = top_5_high_profit_segments

    # Calculate total sales and profit
    sales_total = sum(df['distribution of sales'])
    profit_total = sum(df['distribution of profit'])

    # Normalize sales and profit to ensure they don't exceed 100%
    df['normalized_sales'] = df['distribution of sales'] / sales_total * 100
    df['normalized_profit'] = df['distribution of profit'] / profit_total * 100

    # Prepare the data for the chart
    chart_data = pd.DataFrame({
        'segment': df['segment'].tolist() * 2,  # Duplicate categories for both Sales and Profit
        'value': df['normalized_sales'].tolist() + df['normalized_profit'].tolist(),  # Combine normalized sales and profit values
        'type': ['Sales'] * len(df) + ['Profit'] * len(df)  # Indicate type (Sales or Profit)
    })

    # Create the sunburst chart with updated color scheme
    fig = px.sunburst(
        chart_data,
        path=['type', 'segment'],  # Define hierarchy: first 'type' (Sales or Profit), then 'segment'
        values='value',  # Use the normalized value for size
        title="Segment Sales and Profit Distribution",
        color='type',  # Color by type (Sales, Profit)
        color_discrete_map={'Sales': '#0029ff', 'Profit': '#ff0000'}  # Updated colors: Blue for Sales, Red for Profit
    )

    # Update traces to show both labels and values for child nodes (categories)
    fig.update_traces(
        texttemplate='<b>%{label}</b><br>%{value:.1f}%',  # Show percentages with 1 decimal point
        hovertemplate='<b>Distribution: %{value:.1f}%</b><br>%{label}'  # Show label and value for each segment
    )

    # Update the layout
    fig.update_layout(
        title_font_size=14,
        width=350,
        height=350,
        margin=dict(t=30, l=0, r=0, b=0)
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True, key="donut2")




col7, col8 = st.columns([1, 1])

with col7:
    df = store_records[store_records['year'] == selected_year]
    gp_states_sales = sales_by_state(df)
    gp_states_sales['state_abbrev'] = gp_states_sales['state'].map(states_abbreviation)
    gp_states_sales = gp_states_sales.rename(columns={'state_abbrev':'location'})

    # Custom blue to white color scale
    custom_blue_to_white_scale = [(0, '#ffffff'), (1, '#0029ff')]  # White for 0 sales, deep blue for high sales

    # Create a map
    map1 = px.choropleth(
        gp_states_sales,
        locations='location',
        locationmode='USA-states',
        color='sales',
        scope='usa',
        hover_name='state',
        color_continuous_scale=custom_blue_to_white_scale  # Apply the custom scale from white to blue
    )

    # Update layout
    map1.update_layout(title_text="Sales by State", title_x=0.5, height=325)
    
    # Display the map in Streamlit
    st.plotly_chart(map1, key="map1")



   

with col8:
    df = store_records[store_records['year'] == selected_year]
    gp_states_profit = profits_by_state(df)
    gp_states_profit['state_abbrev'] = gp_states_profit['state'].map(states_abbreviation)
    gp_states_profit = gp_states_profit.rename(columns={'state_abbrev':'location'})

    # Set the color scale to ensure the color changes exactly at zero
    color_scale = [[0, 'red'], [0.5, 'lightgray'], [1, 'blue']]

    # Ensure color midpoint is exactly at zero
    map2 = px.choropleth(
        gp_states_profit,
        locations='location',
        locationmode='USA-states',
        color='profit',
        scope='usa',
        hover_name='state',
        color_continuous_scale=color_scale,
        range_color=[gp_states_profit['profit'].min(), gp_states_profit['profit'].max()],  # Range for the color scale
        color_continuous_midpoint=0  # Set zero as the midpoint
    )

    # Update layout
    map2.update_layout(title_text="Profits by State", title_x=0.5, height=325)
    
    # Display the map in Streamlit
    st.plotly_chart(map2, key="map2")









    

 
 









    

 
 
