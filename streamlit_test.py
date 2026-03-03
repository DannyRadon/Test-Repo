# Import Pool
import streamlit as st

# Testing Section

st.title("SPICE Dashboard Prototype Version 0.01")

st.header("HEADER TEST 1")
st.write("Testing Writing Command - DATA UNDER HEADER 1")

value = st.slider("Choose a Number:", 0, 100, 50)
st.write("You have Selected:", value)

st.header("HEADER TEST 2")
st.write("Testing Writing Command - DATA UNDER HEADER 2")

box_sel = st.selectbox("Select Month:", ['Jan', 'Feb', 'Mar'])
st.write("You have Selected:", box_sel)

st.header("HEADER TEST 3")
st.write("Testing Another Thing Again")

mp_sel = st.multiselect("Select Year(s):", ['2020', '2021', '2022', '2023'])