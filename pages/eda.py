# ---------------------------------------- Test File for Side-Bar Navigation  --------------------------------------------------------

# Import Pool
import streamlit as st
from helpers.data_load import load_data

# Loading in the Data (If Not Cached)
df = load_data()

# Title for the Page
st.title("S.P.I.C.E. - Exploratory Data Analysis Page")

# First Header for the EDA Page
st.header("EDA 1 - Bar Chart (Daily Output Values in kWh)")
st.bar_chart(df['Daily Value (kWh)'])

# Testing Input Columns

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Yield", "12,430 kWh")

with col2:
    st.metric("CO₂ Saved", "3.4 tons")

with col3:
    st.metric("Full Load Hours", "15.7")

# Testing Out Tabs Here...

tab1, tab2 = st.tabs(["Daily", "Monthly"])

with tab1:
    st.write("TESTING THE DAILY TAB")

with tab2:
    st.write("TESTING THE MONTHLY TAB")