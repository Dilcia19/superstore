"""
Streamlit app for Superstore Dashboard
"""

import streamlit as st
import pandas as pd
from superstore_analysis import profit_delta

store_records = pd.read_csv('data/sample_superstore_updated.csv')


col1, col2, col3, col4, col5 = st.columns(5)

profit_delta_dict = profit_delta(store_records)

with col1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")

with col4:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")

with col5:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")