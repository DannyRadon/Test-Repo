# Import Pool
import streamlit as st

# Testing Section


st.write("Testing Writing Command")

value = st.slider("Choose a Number:", 0, 100, 50)

st.write("You have Selected:", value)
