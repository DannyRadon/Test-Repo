# Import Pool
import streamlit as st
from helpers.data_load import load_data


# Initializing the Data into Dashboard
df = load_data()


# --------------- Testing Section ----------------------------

st.title("SPICE Dashboard Prototype v0.01")
st.metric("Total Yield", "12,430 kWh", "+5%")

st.header("HEADER TEST 1")
st.write("Testing HEADER 1 Data Section - Making a Line Graph from Cached DataFrame")

st.write("Checking the DataFrame:", df.head())
st.line_chart(df["Daily Value (kWh)"])

value = st.slider("Choose a Number:", 0, 100, 50)
st.write("You have Selected:", value)


st.header("HEADER TEST 2")
st.write("Testing HEADER 2 Data - Making a Bar Chat with the Same Data (Daily Output in kWh)")
st.bar_chart(df["Daily Value (kWh)"])

box_sel = st.selectbox("Select Month:", ['Jan', 'Feb', 'Mar'])
st.write("You have Selected:", box_sel)


st.header("HEADER TEST 3")
st.write("Testing Another Thing Again")

mp_sel = st.multiselect("Select Year(s):", ['2020', '2021', '2022', '2023'])
date = st.date_input("Select Date")

if st.button("Press Here"):
    st.write("BOOM!")