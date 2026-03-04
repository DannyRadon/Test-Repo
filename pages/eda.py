# ---------------------------------------- Test File for Side-Bar Navigation  --------------------------------------------------------

# Import Pool
import streamlit as st
import plotly.express as px

from helpers.data_load import load_data
from helpers.data_funcs import *

# Loading in the Data (If Not Cached)
df = load_data()

# Title for the Page
st.title("S.P.I.C.E. - Exploratory Data Analysis Page")


# Setting up Tabs on EDA Page
tab1, tab2, tab3 = st.tabs(["Overview", "Monthly Sums", "Daily Cumulative"])

with tab1:

    st.write("Dataset Description")
    st.write(df.describe())

    st.write("Dataset Null Count")
    st.write(df.isnull().sum())
    
    st.write("Default Visualization - Daily Value over Time")
    st.bar_chart(df['Daily Value (kWh)'])

with tab2:
    st.dataframe(monthly_output_sums(df))

with tab3:
    st.dataframe(daily_cumulitive(df))
    st.line_chart(daily_cumulitive(df)['Cumulative Daily'])



# First Header for the EDA Page
st.header("EDA 1 Test - Monthly Sum Interactive Chart")
st.subheader("Monthly Generation Output (kWh)")

fig = px.line(monthly_output_sums(df), x='Date', y='Daily Value (kWh)', title="Monthly Sums of Generation Over Time")
st.plotly_chart(fig)

# Second Header for the EDA Page
st.header("EDA 2 - SOMETHING ELSE")
