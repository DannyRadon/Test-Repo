# Import Pool
import streamlit as st

from helpers.data_load import *
from helpers.data_funcs import *

# Initializing the Data into Dashboard
df = load_data()


# --------------- Building Section ---------------------------- 

st.title("SPICE Dashboard Prototype v0.01")


# Testing Input Columns -- Used for KPI Style Metric Outputs

col1, col2, col3 = st.columns(3)

with col1:
    total_gen = df['Daily Value (kWh)'].sum()
    st.metric("Total Generation (kWh)", f"{total_gen:,.0f}")

with col2:
    total_hours = total_load_hours(df)
    st.metric("Total Load Hours", f"{total_hours:,.0f}")

with col3:
    st.metric("Full Load Hours", "15.7")


st.header("HEADER TEST 1")
st.write("Testing HEADER 1 Data Section - Making a Line Graph from Cached DataFrame")

st.write("Checking the DataFrame:", df.head())

value = st.slider("Choose a Number:", 0, 100, 50)
st.write("You have Selected:", value)


st.header("HEADER TEST 2")
st.write("Testing HEADER 2 Data - Making a Bar Chat with the Same Data (Daily Output in kWh)")

box_sel = st.selectbox("Select Month:", ['Jan', 'Feb', 'Mar'])
st.write("You have Selected:", box_sel)


st.header("HEADER TEST 3")
st.write("Testing Another Thing Again")

mp_sel = st.multiselect("Select Year(s):", ['2020', '2021', '2022', '2023'])
date = st.date_input("Select Date")

if st.button("Press Here"):
    st.write("BOOM!")